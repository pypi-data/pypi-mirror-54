# Princeton University licenses this file to You under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.  You may obtain a copy of the License at:
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.


# *********************************************  ControlProjection *********************************************************

"""
.. _ControlProjection_Overview:

Overview
--------

A ControlProjection is a type of `ModulatoryProjection <ModulatoryProjection>` that projects to the `ParameterPort
<ParameterPort>` of a `ProcessingMechanism <ProcessingMechanism>`. It takes the `value <ControlSignal.value>` of a
`ControlSignal` of a `ControlMechanism <ControlMechanism>` and uses it to  modify the value of the parameter associated
with the ParameterPort to which it projects.  All of the ControlProjections in a Composition, along with its other
`control components <ControlMechanism>`, can be displayed using the Composition's `show_graph <Composition.show_graph>`
method with its **show_control** argument assigned as `True`.

.. _ControlProjection_Creation:

Creating a ControlProjection
----------------------------

A ControlProjection can be created using any of the standard ways to `create a Projection <Projection_Creation>`,
or by including it in a `tuple <ParameterPort_Tuple_Specification>` that specifies a parameter for a `Mechanism
<Mechanism>`, `MappingProjection`, or the `function <Component.function>` of either of these.  If a ControlProjection
is created explicitly (using its constructor), and either its **receiver** or **sender** argument is not specified,
its initialization is `deferred <ControlProjection_Deferred_Initialization>`.  If it is included in a `parameter
specification <ParameterPort_Specification>`, the  `ParameterPort` for the parameter being specified will be assigned
as the ControlProjection's `receiver <ControlProjection.receiver>`.
COMMENT:
TBI FOR COMPOSITION
If the **receiver** belongs to a Mechanism that is part of a `System`, then the ControlProjection's
`sender <ControlProjection.sender>` is assigned to a `ControlSignal` of the System's `controller`.  Otherwise,
its initialization is `deferred <ControlProjection_Deferred_Initialization>`.
COMMENT

.. _ControlProjection_Deferred_Initialization:

*Deferred Initialization*
~~~~~~~~~~~~~~~~~~~~~~~~~

When a ControlProjection is created, its full initialization is `deferred <Component_Deferred_Init>` until its `sender
<ControlProjection.sender>` and `receiver <ControlProjection.receiver>` have been fully specified.  This allows
a ControlProjection to be created before its `sender <ControlProjection.sender>` and/or `receiver
<ControlProjection.receiver>` have been created (e.g., before them in a script), by calling its constructor without
specifying its **sender** or **receiver** arguments. However, for the ControlProjection to be operational,
initialization must be completed by a call to its `deferred_init` method. This is done automatically if the
ControlProjection is included in a `tuple specification <ParameterPort_Tuple_Specification>` for the parameter of a
`Mechanism <Mechanism>` or its `function <Mechanism_Base.function>`, when the `ControlMechanism <ControlMechanism>`
is created for the `Composition` to which the parameter's owner belongs (see `ControlMechanism_Creation`).


.. _ControlProjection_Structure:

Structure
---------

The `sender <ControlProjection.sender>` of a ControlProjection is a `ControlSignal` of a `ControlMechanism
<ControlMechanism>`. The `value <ControlSignal.value>` of the `sender <ControlProjection.sender>` is used by the
ControlProjection as its `variable <ControlProjection.variable>`;  this is also assigned to its `control_signal
<ControlProjection.control_signal>` attribute, and serves as the input to the ControlProjection's `function
<ControlProjection.function>`.  The default `function <ControlProjection.function>` for a
ControlProjection is an identity function (`Linear` with **slope**\\ =1 and **intercept**\\ =0);  that is, it simply
conveys the value of its `control_signal <ControlProjection.control_signal>` to its `receiver
<ControlProjection.receiver>`, for use in modifying the value of the parameter that it controls. Its `receiver
<ControlProjection.receiver>` is the `ParameterPort` for the parameter of the `Mechanism <Mechanism>` or its `function
<Mechanism_Base.function>` that is controlled by the ControlProjection.

.. _ControlProjection_Execution:

Execution
---------

A ControlProjection cannot be executed directly.  It is executed when the `ParameterPort` to which it projects is
updated.  Note that this only occurs when the `Mechanism <Mechanism>` to which the `ParameterPort` belongs is executed
(see :ref:`Lazy Evaluation <LINK>` for an explanation of "lazy" updating). When a ControlProjection is executed, its
`function <ControlProjection.function>` gets the `control_signal <ControlProjection.control_signal>` from its `sender
<ControlProjection.sender>` and conveys that to its `receiver <ControlProjection.receiver>`.  This is used by the
`receiver <ControlProjection.receiver>` to modify the parameter controlled by the ControlProjection (see
`ModulatorySignal_Modulation` and `ParameterPort Execution <ParameterPort_Execution>` for how modulation operates and
how this applies to a ParameterPort).

.. note::
   The changes to a parameter in response to the execution of a ControlProjection are not applied until the `Mechanism
   <Mechanism>` that receives the ControlProjection are next executed; see :ref:`Lazy Evaluation` for an explanation of
   "lazy" updating).

.. _ControlProjection_Class_Reference:


Class Reference
---------------

"""

import inspect

import typecheck as tc

from psyneulink.core.components.component import parameter_keywords
from psyneulink.core.components.functions.transferfunctions import Linear
from psyneulink.core.components.mechanisms.modulatory.control.controlmechanism import ControlMechanism
from psyneulink.core.components.projections.modulatory.modulatoryprojection import ModulatoryProjection_Base
from psyneulink.core.components.projections.projection import ProjectionError, Projection_Base, projection_keywords
from psyneulink.core.components.shellclasses import Mechanism, Process_Base
from psyneulink.core.globals.context import ContextFlags
from psyneulink.core.globals.keywords import \
    CONTROL, CONTROL_PROJECTION, CONTROL_SIGNAL, INPUT_PORT, OUTPUT_PORT, PARAMETER_PORT, PROJECTION_SENDER
from psyneulink.core.globals.parameters import Parameter
from psyneulink.core.globals.preferences.basepreferenceset import is_pref_set
from psyneulink.core.globals.preferences.preferenceset import PreferenceLevel

__all__ = [
    'CONTROL_SIGNAL_PARAMS', 'ControlProjection', 'ControlProjectionError',
]

parameter_keywords.update({CONTROL_PROJECTION, CONTROL})
projection_keywords.update({CONTROL_PROJECTION, CONTROL})

CONTROL_SIGNAL_PARAMS = 'control_signal_params'

class ControlProjectionError(Exception):
    def __init__(self, error_value):
        self.error_value = error_value

    def __str__(self):
        return repr(self.error_value)


def _control_signal_getter(owning_component=None, context=None):
    return owning_component.sender.parameters.value._get(context)


def _control_signal_setter(value, owning_component=None, context=None):
    owning_component.sender.parameters.value._set(value, context, override)
    return value


class ControlProjection(ModulatoryProjection_Base):
    """
    ControlProjection(           \
     sender=None,                \
     receiver=None,              \
     function=Linear,            \
     weight=None,                \
     exponent=None,              \
     control_signal_params=None, \
     params=None,                \
     name=None,                  \
     prefs=None)

    Subclass of `ModulatoryProjection <ModulatoryProjection>` that modulates the value of a `ParameterPort` of a
    `Mechanism <Mechanism>`.

    COMMENT:
        Description:
            The ControlProjection class is a type in the Projection category of Component.
            It implements a projection to the ParameterPort of a Mechanism that modifies a parameter of its function.
            It:
               - takes a scalar as its input (sometimes referred to as an "allocation")
               - uses its `function` to compute its value (sometimes referred to as its "intensity"
                 based on its input (allocation) its `sender`,
               - used to modify a parameter of the owner of the `receiver` or its `function`.

        ** MOVE:
        ProjectionRegistry:
            All ControlProjections are registered in ProjectionRegistry, which maintains an entry for the subclass,
              a count for all instances of it, and a dictionary of those instances

        Class attributes:
            + color (value): for use in interface design
            + classPreference (PreferenceSet): ControlProjectionPreferenceSet, instantiated in __init__()
            + classPreferenceLevel (PreferenceLevel): PreferenceLevel.TYPE
            + paramClassDefaults:
                FUNCTION:Linear,
                FUNCTION_PARAMS:{SLOPE: 1, INTERCEPT: 0},  # Note: this implements identity function
                PROJECTION_SENDER: ControlMechanism
                CONTROL_SIGNAL_COST_OPTIONS:CostFunctions.DEFAULTS,
                ALLOCATION_SAMPLES: DEFAULT_ALLOCATION_SAMPLES,
    COMMENT


    Arguments
    ---------

    sender : Optional[ControlMechanism or ControlSignal]
        specifies the source of the `control_signal <ControlProjection.control_signal>` for the ControlProjection;
        if it is not specified and cannot be `inferred from context <ControlProjection_Creation>`, initialization is
        `deferred <ControlProjection_Deferred_Initialization>`.

    receiver : Optional[Mechanism or ParameterPort]
        specifies the `ParameterPort` associated with the parameter to be controlled; if it is not specified,
        and cannot be `inferred from context <ControlProjection_Creation>`, initialization is `deferred
        <ControlProjection_Deferred_Initialization>`.

    function : TransferFunction : default Linear(slope=1, intercept=0)
        specifies the function used to convert the `control_signal <ControlProjection.control_signal>` to the
        ControlProjection's `value <ControlProjection.value>`.

    weight : number : default None
       specifies the value by which to multiply the ControlProjection's `value <ControlProjection.value>`
       before combining it with others (see `weight <ControlProjection.weight>` for additional details).

    exponent : number : default None
       specifies the value by which to exponentiate the ControlProjection's `value <ControlProjection.value>`
       before combining it with others (see `exponent <ControlProjection.exponent>` for additional details).

    control_signal_params pip install --updgrade Sphinx==1.6.2 sphinx-rtd-theme==0.2.4 sphinxcontrib-websupport==1.0.1: Dict[param keyword: param value]
        a `parameter dictionary <ParameterPort_Specification>` that can be used to specify the parameters for the
        ControlProjection's `sender <ControlProjection.sender>` (see `ControlSignal_Structure` for a description
        of ControlSignal parameters).

    params : Dict[param keyword: param value] : default None
        a `parameter dictionary <ParameterPort_Specification>` that can be used to specify the parameters for
        the ControlProjection, its `function <ControlProjection.function>`, and/or a custom function and its parameters.
        Values specified for parameters in the dictionary override any assigned to those parameters in arguments of the
        constructor.

    name : str : default see ModulatoryProjection `name <ModulatoryProjection_Base.name>`
        specifies the name of the ControlProjection.

    prefs : PreferenceSet or specification dict : default Projection.classPreferences
        specifies the `PreferenceSet` for the ControlProjection; see `prefs <ControlProjection.prefs>` for details.

    Attributes
    ----------

    componentType : CONTROL_PROJECTION

    sender : ControlSignal
        source of the `control_signal <ControlProjection.control_signal>`.

    receiver : ParameterPort of Mechanism
        `ParameterPort` for the parameter to be modified by the ControlProjection.

    variable : 2d np.array
        same as `control_signal <ControlProjection.control_signal>`.

    control_signal : 1d np.array
        the `value <ControlSignal.value>` of the ControlProjection's `sender <ControlProjection.sender>`.

    function : Function
        assigns the `control_signal` received from the `sender <ControlProjection.sender>` to the
        ControlProjection's `value <ControlProjection.value>`; the default in an identity function.

    value : float
        the value used to modify the parameter controlled by the ControlProjection (see `ModulatorySignal_Modulation`
        and `ParameterPort Execution <ParameterPort_Execution>` for how modulation operates and how this applies
        to a ParameterPort).

    weight : number
       multiplies the `value <ControlProjection.value>` of the ControlProjection after applying `exponent
       <ControlProjection.exponent>`, and before combining it with any others that project to the same `ParameterPort`
       to determine how that ParameterPort's `variable <ParameterPort.variable>` is modified (see description in
       `Projection <Projection_Weight_Exponent>` for details).

    exponent : number
        exponentiates the `value <ControlProjection.value>` of the ControlProjection, before applying `weight
        <ControlProjection.weight>`, and before combining it with any others that project to the same `ParameterPort`
        to determine how that ParameterPort's `variable <ParameterPort.variable>` is modified (see description in
        `Projection <Projection_Weight_Exponent>` for details).

    name : str
        name of the ControlProjection; if it is not specified in the **name** argument of its constructor,
        a default name is assigned (see ModulatoryProjection `name <ModulatoryProjection_Base.name>`;
        also see `Naming` for conventions regarding duplicate names).

    prefs : PreferenceSet or specification dict
        the `PreferenceSet` for the ControlProjection; if it is not specified in the **prefs** argument of the
        constructor, a default is assigned using `classPreferences` defined in __init__.py (see :doc:`PreferenceSet
        <LINK>` for details).
    """

    color = 0

    componentType = CONTROL_PROJECTION
    className = componentType
    suffix = " " + className

    classPreferenceLevel = PreferenceLevel.TYPE

    class sockets:
        sender=[CONTROL_SIGNAL]
        receiver=[PARAMETER_PORT, INPUT_PORT, OUTPUT_PORT]

    class Parameters(ModulatoryProjection_Base.Parameters):
        """
            Attributes
            ----------

                control_signal
                    see `control_signal <ControlProjection.control_signal>`

                    :default value: None
                    :type:
                    :read only: True

                function
                    see `function <ControlProjection.function>`

                    :default value: `Linear`
                    :type: `Function`

        """
        function = Parameter(Linear, stateful=False, loggable=False)
        control_signal = Parameter(None, read_only=True, getter=_control_signal_getter, setter=_control_signal_setter, pnl_internal=True)

        control_signal_params = Parameter(
            None,
            stateful=False,
            loggable=False,
            read_only=True,
            user=False,
            pnl_internal=True
        )

    paramClassDefaults = Projection_Base.paramClassDefaults.copy()
    paramClassDefaults.update({
        PROJECTION_SENDER: ControlMechanism,
    })

    @tc.typecheck
    def __init__(self,
                 sender=None,
                 receiver=None,
                 weight=None,
                 exponent=None,
                 function=Linear,
                 control_signal_params:tc.optional(dict)=None,
                 params=None,
                 name=None,
                 prefs:is_pref_set=None,
                 **kwargs):
        # Assign args to params and functionParams dicts
        params = self._assign_args_to_param_dicts(function=function,
                                                  control_signal_params=control_signal_params,
                                                  params=params)

        # If receiver has not been assigned, defer init to Port.instantiate_projection_to_state()
        if (sender is None or sender.initialization_status == ContextFlags.DEFERRED_INIT or
                inspect.isclass(receiver) or receiver is None or
                    receiver.initialization_status == ContextFlags.DEFERRED_INIT):
            self.initialization_status = ContextFlags.DEFERRED_INIT

        # Validate sender (as variable) and params, and assign to variable and paramInstanceDefaults
        # Note: pass name of mechanism (to override assignment of componentName in super.__init__)
        # super(ControlSignal_Base, self).__init__(sender=sender,
        super(ControlProjection, self).__init__(sender=sender,
                                                receiver=receiver,
                                                weight=weight,
                                                exponent=exponent,
                                                function=function,
                                                params=params,
                                                name=name,
                                                prefs=prefs,
                                                **kwargs)

    def _instantiate_sender(self, sender, params=None, context=None):
        """Check if DefaultController is being assigned and if so configure it for the requested ControlProjection

        If self.sender is a Mechanism, re-assign to <Mechanism>.outputPort
        Insure that sender.value = self.defaults.variable

        This method overrides the corresponding method of Projection, before calling it, to check if the
            DefaultController is being assigned as sender and, if so:
            - creates projection-dedicated inputPort and outputPort in DefaultController
            - puts them in DefaultController's input_ports and outputPorts attributes
            - lengthens variable of DefaultController to accommodate the ControlProjection
            - updates value of the DefaultController (in response to the new variable)
        Notes:
            * the default function of the DefaultControlMechanism simply maps the inputPort value to the outputPort
            * the params arg is assumed to be a dictionary of params for the ControlSignal of the ControlMechanism

        :return:
        """

        # A Process can't be the sender of a ControlMechanism
        if isinstance(sender, Process_Base):
            raise ProjectionError(
                "PROGRAM ERROR: attempt to add a ControlProjection from a Process {0} "
                "to a Mechanism {0} in pathway list".format(self.name, sender.name)
            )

        # If sender is specified as a Mechanism, validate that it is a ControlMechanism
        if isinstance(sender, Mechanism):
            # If sender is a ControlMechanism, call it to instantiate its ControlSignal projection
            if not isinstance(sender, ControlMechanism):
                raise ControlProjectionError(
                    "Mechanism specified as sender for {} ({}) must be a "
                    "ControlMechanism (but it is a {})".format(
                        self.name, sender.name, sender.__class__.__name__
                    )
                )

        # Call super to instantiate sender
        super()._instantiate_sender(sender, context=context)


    def _instantiate_receiver(self, context=None):
        # FIX: THIS NEEDS TO BE PUT BEFORE _instantiate_function SINCE THAT USES self.receiver
        """Handle situation in which self.receiver was specified as a Mechanism (rather than Port)

        Overrides Projection._instantiate_receiver, to require that if the receiver is specified as a Mechanism, then:
            the receiver Mechanism must have one and only one ParameterPort;
            otherwise, passes control to Projection_Base._instantiate_receiver for validation

        :return:
        """
        if isinstance(self.receiver, Mechanism):
            # If there is just one param of ParameterPort type in the receiver Mechanism
            # then assign it as actual receiver (which must be a Port);  otherwise, raise exception
            from psyneulink.core.components.ports.parameterport import ParameterPort
            if len(dict((param_name, port) for param_name, port in self.receiver.paramsCurrent.items()
                    if isinstance(port, ParameterPort))) == 1:
                receiver_parameter_port = [port for port in dict.values()][0]
                # Reassign self.receiver to Mechanism's parameterPort
                self.receiver = receiver_parameter_port
            else:
                raise ControlProjectionError("Unable to assign ControlProjection ({0}) from {1} to {2}, "
                                         "as it has several ParameterPorts;  must specify one (or each) of them"
                                         " as receiver(s)".
                                         format(self.name, self.sender.owner, self.receiver.name))
        # else:
        super(ControlProjection, self)._instantiate_receiver(context=context)

    # def _execute(self, variable=None, context=None, runtime_params=None):
    #     return super()._execute(variable, context, runtime_params)

    @property
    def control_signal(self):
        return self.sender.value
