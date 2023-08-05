# Princeton University licenses this file to You under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.  You may obtain a copy of the License at:
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.


# *********************************************  GatingProjection ******************************************************

"""
.. _GatingProjection_Overview:

Overview
--------

A GatingProjection is a type of `ModulatoryProjection <ModulatoryProjection>` that projects to the `InputPort` or
`OutputPort` of a `Mechanism <Mechanism>`. It takes the value of a `GatingSignal` of a `GatingMechanism`,
and uses it to modulate the `value <Port_Base.value>` of the Port to which it projects.

.. _GatingProjection_Creation:

Creating a GatingProjection
----------------------------

A GatingProjection can be created using any of the standard ways to `create a projection <Projection_Creation>`,
or by including it in the specification of an `InputPort <InputPort_Projection_Source_Specification>` or `OutputPort
<OutputPort_Projections>` .  If a GatingProjection is created explicitly (using its constructor), its **receiver**
argument can be specified as a particular InputPort or OutputPort of a designated `Mechanism <Mechanism>`, or simply
as the Mechanism.  In the latter case, the Mechanism's `primary InputPort <InputPort_Primary>` will be used. If the
GatingProjection is included in an InputPort or OutputPort specification, that Port will be assigned as the
GatingProjection's `receiver <GatingProjection.receiver>`. If the **sender** and/or **receiver** arguments are not
specified, its initialization is `deferred <GatingProjection_Deferred_Initialization>`.


.. _GatingProjection_Deferred_Initialization:

*Deferred Initialization*
~~~~~~~~~~~~~~~~~~~~~~~~~

When a GatingProjection is created, its full initialization is `deferred <Component_Deferred_Init>` until its
`sender <ControlProjection.sender>` and `receiver <ControlProjection.receiver>` have been fully specified.  This allows
a GatingProjection to be created before its `sender` and/or `receiver` have been created (e.g., before them in a
script), by calling its constructor without specifying its **sender** or **receiver** arguments. However, for the
GatingProjection to be operational, initialization must be completed by calling its `deferred_init` method.  This is
not necessary if the Port(s) to be gated are specified in the **gate** argument of a `GatingMechanism
<GatingMechanism_Specifying_Gating>`, in which case deferred initialization is completed automatically by the
GatingMechanism when it is created.

.. _GatingProjection_Structure:

Structure
---------

The `sender <GatingProjection.sender>` of a GatingProjection is a `GatingSignal` of a `GatingMechanism`.  The `value
<GatingSignal.value>` of the `sender <GatingProjection.sender>` is used by the GatingProjection as its
`variable <GatingProjection.variable>`;  this is also assigned to its `gating_signal
<GatingProjection.gating_signal>` attribute, and serves as the input to the GatingProjection's `function
<GatingProjection.function>`.  The default `function <GatingProjection.function>` for a
GatingProjection is an identity function (`Linear` with **slope**\\ =1 and **intercept**\\ =0);  that is,
it simply conveys the value of its `gating_signal <GatingProjection.gating_signal>` to its `receiver
<GatingProjection.receiver>`, for use in modifying the `value <Port_Base.value>` of the Port that it gates. Its
`receiver <GatingProjection.receiver>` is the `InputPort` or `OutputPort` of a `Mechanism <Mechanism>`.

.. _GatingProjection_Execution:

Execution
---------

A GatingProjection cannot be executed directly.  It is executed when the `InputPort` or `OutputPort` to which it
projects is updated.  Note that this only occurs when the `Mechanism <Mechanism>` to which the `Port <Port>`
belongs is executed (see :ref:`Lazy Evaluation <LINK>` for an explanation of "lazy" updating). When a GatingProjection
is executed, its `function <GatingProjection.function>` gets the `gating_signal <GatingProjection.gating_signal>` from
its `sender <GatingProjection.sender>` and conveys that to its `receiver <GatingProjection.receiver>`.  This is used by
the `receiver <GatingProjection.receiver>` to modify the `value <Port_Base.value>` of the Port gated by the
GatingProjection (see `ModulatorySignal_Modulation`, `InputPort Execution <InputPort_Execution>` and `OutputPort
Execution <OutputPort_Execution>` for how modulation operates and how this applies to a InputPorts and OutputPorts).

.. note::
   The changes in an InputPort or OutputPort's `value <Port_Base.value >` in response to the execution of a
   GatingProjection are not applied until the Mechanism to which the Port belongs is next executed;
   see :ref:`Lazy Evaluation` for an explanation of "lazy" updating).

.. _GatingProjection_Class_Reference:

Class Reference
---------------

"""
import typecheck as tc

from psyneulink.core.components.component import parameter_keywords
from psyneulink.core.components.functions.function import FunctionOutputType
from psyneulink.core.components.functions.transferfunctions import Linear
from psyneulink.core.components.mechanisms.modulatory.control.gating.gatingmechanism import GatingMechanism
from psyneulink.core.components.projections.modulatory.modulatoryprojection import ModulatoryProjection_Base
from psyneulink.core.components.projections.projection import ProjectionError, Projection_Base, projection_keywords
from psyneulink.core.components.shellclasses import Mechanism, Process_Base
from psyneulink.core.globals.context import ContextFlags
from psyneulink.core.globals.keywords import \
    FUNCTION_OUTPUT_TYPE, GATING, GATING_MECHANISM, GATING_PROJECTION, GATING_SIGNAL, \
    INPUT_PORT, OUTPUT_PORT, PROJECTION_SENDER
from psyneulink.core.globals.parameters import Parameter
from psyneulink.core.globals.preferences.basepreferenceset import is_pref_set
from psyneulink.core.globals.preferences.preferenceset import PreferenceLevel

__all__ = [
    'GATING_SIGNAL_PARAMS', 'GatingProjection', 'GatingProjectionError',
]

parameter_keywords.update({GATING_PROJECTION, GATING})
projection_keywords.update({GATING_PROJECTION, GATING})
GATING_SIGNAL_PARAMS = 'gating_signal_params'

class GatingProjectionError(Exception):
    def __init__(self, error_value):
        self.error_value = error_value

    def __str__(self):
        return repr(self.error_value)


def _gating_signal_getter(owning_component=None, context=None):
    return owning_component.sender.parameters.value._get(context)


def _gating_signal_setter(value, owning_component=None, context=None):
    owning_component.sender.parameters.value._set(value, context)
    return value


class GatingProjection(ModulatoryProjection_Base):
    """
    GatingProjection(           \
     sender=None,               \
     receiver=None,             \
     function=Linear            \
     weight=None,               \
     exponent=None,             \
     gating_signal_params=None, \
     params=None,               \
     name=None,                 \
     prefs=None)

    Subclass of `ModulatoryProjection <ModulatoryProjection>` that modulates the value of an `InputPort` or
    `OutputPort`.

    COMMENT:
        Description:
            The GatingProjection class is a type in the Projection category of Component.
            It implements a projection to the InputPort or OutputPort of a Mechanism that modulates the value of
            that port
            It:
               - takes a scalar as its input (sometimes referred to as a "gating signal")
               - uses its `function` to compute its value
               - its value is used to modulate the value of the port to which it projects

        ** MOVE:
        ProjectionRegistry:
            All GatingProjections are registered in ProjectionRegistry, which maintains an entry for the subclass,
              a count for all instances of it, and a dictionary of those instances

        Class attributes:
            + color (value): for use in interface design
            + classPreference (PreferenceSet): GatingProjectionPreferenceSet, instantiated in __init__()
            + classPreferenceLevel (PreferenceLevel): PreferenceLevel.TYPE
            + paramClassDefaults:
                FUNCTION:Linear,
                FUNCTION_PARAMS:{SLOPE: 1, INTERCEPT: 0},  # Note: this implements identity function
                PROJECTION_SENDER: DefaultGatingMechanism, # GatingProjection (assigned to class ref in __init__ module)
    COMMENT


    Arguments
    ---------

    sender : Optional[GatingMechanism or GatingSignal]
        specifies the source of the `gating_signal <GatingProjection.gating_signal>` for the GatingProjection;
        if it is not specified and cannot be `inferred from context <GatingProjection_Creation>` , initialization is
        `deferred <GatingProjection_Deferred_Initialization>`.

    receiver : Optional[Mechanism, InputPort or OutputPort]
        specifies the `InputPort` or `OutputPort` to which the GatingProjection projects; if it is not specified,
        and cannot be `inferred from context <GatingProjection_Creation>`, initialization is `deferred
        <GatingProjection_Deferred_Initialization>`.

    function : TransferFunction : default Linear(slope=1, intercept=0)
        specifies the function used to convert the `gating_signal <GatingProjection.gating_signal>` to the
        GatingProjection's `value <GatingProjection.value>`.

    weight : number : default None
       specifies the value by which to multiply the GatingProjection's `value <GatingProjection.value>`
       before combining it with others (see `weight <GatingProjection.weight>` for additional details).

    exponent : number : default None
       specifies the value by which to exponentiate the GatingProjection's `value <GatingProjection.value>`
       before combining it with others (see `exponent <GatingProjection.exponent>` for additional details).

    gating_signal_params : Dict[param keyword: param value]
        a `parameter dictionary <ParameterPort_Specification>` that can be used to specify the parameters for the
        GatingProjection's `sender <ControlProjection.sender>` (see `GatingSignal_Structure` for a description
        of GatingSignal parameters).

    params : Dict[param keyword: param value] : default None
        a `parameter dictionary <ParameterPort_Specification>` that can be used to specify the parameters for
        the GatingProjection, its `function <GatingProjection.function>`, and/or a custom function and its parameters.
        Values specified for parameters in the dictionary override any assigned to those parameters in arguments of the
        constructor.

    name : str : default see ModulatoryProjection `name <ModulatoryProjection_Base.name>`
        specifies the name of the GatingProjection.

    prefs : PreferenceSet or specification dict : default Projection.classPreferences
        specifies the `PreferenceSet` for the GatingProjection; see `prefs <GatingProjection.prefs>` for details.

    Attributes
    ----------

    componentType : GATING_PROJECTION

    sender : GatingSignal
        source of the `gating_signal <GatingProjection.gating_signal>`.

    receiver : InputPort or OutputPort of a Mechanism
        `InputPort` or `OutputPort` to which the GatingProjection projects.

    variable : 2d np.array
        same as `gating_signal <GatingProjection.gating_signal>`.

    gating_signal : 1d np.array
        the `value <GatingSignal.value>` of the GatingProjection's `sender <GatingProjection.sender>`.

    function : Function
        assigns the `gating_signal` received from the `sender <GatingProjection.sender>` to the
        GatingProjection's `value <GatingProjection.value>`; the default is an identity function.

    value : float
        the value used to modify the `value <Port_Base.value>` of the `InputPort` or `OutputPort` gated by the
        GatingProjection (see `ModulatorySignal_Modulation`, `InputPort Execution <InputPort_Execution>`, and
        `OutputPort Execution <OutputPort_Execution>` for how modulation operates and how this applies to InputPorts
        and OutputPorts).

    weight : number
       multiplies the `value <GatingProjection.value>` of the GatingProjection after applying `exponent
       <GatingProjection.exponent>`, and before combining it with any others that project to the same `InputPort`
       or `OutputPort` to determine how that Port's `variable <Port.variable>` is modified (see description in
       `Projection <Projection_Weight_Exponent>` for details).

    exponent : number
        exponentiates the `value <GatingProjection.value>` of the GatingProjection, before applying `weight
        <ControlProjection.weight>`, and before combining it with any others that project to the same `InputPort`
       or `OutputPort` to determine how that Port's `variable <Port.variable>` is modified (see description in
       `Projection <Projection_Weight_Exponent>` for details).

    name : str
        name of the GatingProjection; if it is not specified in the **name** argument of its constructor,
        a default name is assigned (see ModulatoryProjection `name <ModulatoryProjection_Base.name>`;
        also see `Naming` for conventions regarding duplicate names).

    prefs : PreferenceSet or specification dict
        the `PreferenceSet` for the GatingProjection; if it is not specified in the **prefs** argument of the
        constructor, a default is assigned using `classPreferences` defined in __init__.py (see :doc:`PreferenceSet
        <LINK>` for details).
    """

    color = 0

    componentType = GATING_PROJECTION
    className = componentType
    suffix = " " + className

    classPreferenceLevel = PreferenceLevel.TYPE

    class sockets:
        sender=[GATING_SIGNAL]
        receiver=[INPUT_PORT, OUTPUT_PORT]

    class Parameters(ModulatoryProjection_Base.Parameters):
        """
            Attributes
            ----------

                function
                    see `function <GatingProjection.function>`

                    :default value: `Linear`
                    :type: `Function`

                gating_signal
                    see `gating_signal <GatingProjection.gating_signal>`

                    :default value: None
                    :type:
                    :read only: True

        """
        function = Parameter(Linear(params={FUNCTION_OUTPUT_TYPE: FunctionOutputType.RAW_NUMBER}), stateful=False, loggable=False)
        gating_signal = Parameter(None, read_only=True, getter=_gating_signal_getter, setter=_gating_signal_setter, pnl_internal=True)

    paramClassDefaults = Projection_Base.paramClassDefaults.copy()
    paramClassDefaults.update({
        PROJECTION_SENDER: GatingMechanism,
    })

    @tc.typecheck
    def __init__(self,
                 sender=None,
                 receiver=None,
                 function=Linear(params={FUNCTION_OUTPUT_TYPE:FunctionOutputType.RAW_NUMBER}),
                 weight=None,
                 exponent=None,
                 gating_signal_params:tc.optional(dict)=None,
                 params=None,
                 name=None,
                 prefs:is_pref_set=None,
                 **kwargs
                 ):
        # Assign args to params and functionParams dicts
        params = self._assign_args_to_param_dicts(function=function,
                                                  gating_signal_params=gating_signal_params,
                                                  params=params)

        # If receiver has not been assigned, defer init to Port.instantiate_projection_to_state()
        if sender is None or receiver is None:
            # Flag for deferred initialization
            self.initialization_status = ContextFlags.DEFERRED_INIT

        # Validate sender (as variable) and params, and assign to variable and paramInstanceDefaults
        # Note: pass name of mechanism (to override assignment of componentName in super.__init__)
        super().__init__(sender=sender,
                         receiver=receiver,
                         weight=weight,
                         exponent=exponent,
                         function=function,
                         params=params,
                         name=name,
                         prefs=prefs,
                         **kwargs)

    def _instantiate_sender(self, sender, params=None, context=None):
        """Check that sender is not a process and that, if specified as a Mechanism, it is a GatingMechanism
        """

        # A Process can't be the sender of a GatingProjection
        if isinstance(sender, Process_Base):
            raise ProjectionError(
                "PROGRAM ERROR: attempt to add a {} from a Process {0} "
                "to a Mechanism {0} in pathway list".format(
                    GATING_PROJECTION, self.name, sender.name
                )
            )

        # If sender is specified as a Mechanism, validate that it is a GatingMechanism
        if isinstance(sender, Mechanism):
            if not isinstance(sender, GatingMechanism):
                raise GatingProjectionError(
                    "Mechanism specified as sender for {} ({}) must be a {} (but it is a {})".format(
                        GATING_MECHANISM, self.name, sender.name, sender.__class__.__name__
                    )
                )

        # Call super to instantiate sender
        super()._instantiate_sender(sender, context=context)

    def _validate_params(self, request_set, target_set=None, context=None):

        super()._validate_params(request_set=request_set, target_set=target_set, context=context)

        if self.initialization_status == ContextFlags.INITIALIZING:
            from psyneulink.core.components.ports.inputport import InputPort
            from psyneulink.core.components.ports.outputport import OutputPort
            if not isinstance(self.receiver, (InputPort, OutputPort, Mechanism)):
                raise GatingProjectionError("Receiver specified for {} {} is not a "
                                            "Mechanism, InputPort or OutputPort".
                                            format(self.receiver, self.name))

    def _instantiate_receiver(self, context=None):
        """Assign port if receiver is Mechanism, and match output to param being modulated
        """
        # If receiver specification was a Mechanism, re-assign to the mechanism's primary inputPort
        if isinstance(self.receiver, Mechanism):
            # If Mechanism is specified as receiver, assign GatingProjection to primary inputPort as the default
            self.receiver = self.receiver.input_ports[0]

        # # Match type of GatingProjection.value to type to the parameter being modulated
        # modulated_param = self.sender.modulation
        # function = self.receiver.function
        # function_param = function.params[modulated_param]
        # function_param_value = function.params[function_param]
        # gating_projection_function = self.function
        # gating_projection_function.output_type = type(function_param_value)
        # # ASSIGN FUNCTION TYPE TO FUNCTION HERE

        super()._instantiate_receiver(context=context)

    @property
    def gating_signal(self):
        return self.sender.value
