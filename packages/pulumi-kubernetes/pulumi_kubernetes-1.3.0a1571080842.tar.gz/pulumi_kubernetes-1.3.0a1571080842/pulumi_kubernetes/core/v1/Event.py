# *** WARNING: this file was generated by the Pulumi Kubernetes codegen tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
from typing import Optional

import pulumi
import pulumi.runtime
from pulumi import Input, ResourceOptions

from ... import tables, version


class Event(pulumi.CustomResource):
    """
    Event is a report of an event somewhere in the cluster.
    """

    apiVersion: pulumi.Output[str]
    """
    APIVersion defines the versioned schema of this representation of an object. Servers should
    convert recognized schemas to the latest internal value, and may reject unrecognized values.
    More info: https://git.k8s.io/community/contributors/devel/api-conventions.md#resources
    """

    kind: pulumi.Output[str]
    """
    Kind is a string value representing the REST resource this object represents. Servers may infer
    this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More
    info: https://git.k8s.io/community/contributors/devel/api-conventions.md#types-kinds
    """

    action: pulumi.Output[str]
    """
    What action was taken/failed regarding to the Regarding object.
    """

    count: pulumi.Output[int]
    """
    The number of times this event has occurred.
    """

    event_time: pulumi.Output[str]
    """
    Time when this Event was first observed.
    """

    first_timestamp: pulumi.Output[str]
    """
    The time at which the event was first recorded. (Time of server receipt is in TypeMeta.)
    """

    involved_object: pulumi.Output[dict]
    """
    The object that this event is about.
    """

    last_timestamp: pulumi.Output[str]
    """
    The time at which the most recent occurrence of this event was recorded.
    """

    message: pulumi.Output[str]
    """
    A human-readable description of the status of this operation.
    """

    metadata: pulumi.Output[dict]
    """
    Standard object's metadata. More info:
    https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata
    """

    reason: pulumi.Output[str]
    """
    This should be a short, machine understandable string that gives the reason for the transition
    into the object's current status.
    """

    related: pulumi.Output[dict]
    """
    Optional secondary object for more complex actions.
    """

    reporting_component: pulumi.Output[str]
    """
    Name of the controller that emitted this Event, e.g. `kubernetes.io/kubelet`.
    """

    reporting_instance: pulumi.Output[str]
    """
    ID of the controller instance, e.g. `kubelet-xyzf`.
    """

    series: pulumi.Output[dict]
    """
    Data about the Event series this event represents or nil if it's a singleton Event.
    """

    source: pulumi.Output[dict]
    """
    The component reporting this event. Should be a short machine understandable string.
    """

    type: pulumi.Output[str]
    """
    Type of this event (Normal, Warning), new types could be added in the future
    """

    def __init__(self, resource_name, opts=None, involved_object=None, metadata=None, action=None, count=None, event_time=None, first_timestamp=None, last_timestamp=None, message=None, reason=None, related=None, reporting_component=None, reporting_instance=None, series=None, source=None, type=None, __name__=None, __opts__=None):
        """
        Create a Event resource with the given unique name, arguments, and options.

        :param str resource_name: The _unique_ name of the resource.
        :param pulumi.ResourceOptions opts: A bag of options that control this resource's behavior.
        :param pulumi.Input[dict] involved_object: The object that this event is about.
        :param pulumi.Input[dict] metadata: Standard object's metadata. More info:
               https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata
        :param pulumi.Input[str] action: What action was taken/failed regarding to the Regarding object.
        :param pulumi.Input[int] count: The number of times this event has occurred.
        :param pulumi.Input[str] event_time: Time when this Event was first observed.
        :param pulumi.Input[str] first_timestamp: The time at which the event was first recorded. (Time of server receipt is in
               TypeMeta.)
        :param pulumi.Input[str] last_timestamp: The time at which the most recent occurrence of this event was recorded.
        :param pulumi.Input[str] message: A human-readable description of the status of this operation.
        :param pulumi.Input[str] reason: This should be a short, machine understandable string that gives the reason for the
               transition into the object's current status.
        :param pulumi.Input[dict] related: Optional secondary object for more complex actions.
        :param pulumi.Input[str] reporting_component: Name of the controller that emitted this Event, e.g. `kubernetes.io/kubelet`.
        :param pulumi.Input[str] reporting_instance: ID of the controller instance, e.g. `kubelet-xyzf`.
        :param pulumi.Input[dict] series: Data about the Event series this event represents or nil if it's a singleton Event.
        :param pulumi.Input[dict] source: The component reporting this event. Should be a short machine understandable string.
        :param pulumi.Input[str] type: Type of this event (Normal, Warning), new types could be added in the future
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if not resource_name:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(resource_name, str):
            raise TypeError('Expected resource name to be a string')
        if opts and not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        __props__['apiVersion'] = 'v1'
        __props__['kind'] = 'Event'
        if involved_object is None:
            raise TypeError('Missing required property involved_object')
        __props__['involvedObject'] = involved_object
        if metadata is None:
            raise TypeError('Missing required property metadata')
        __props__['metadata'] = metadata
        __props__['action'] = action
        __props__['count'] = count
        __props__['eventTime'] = event_time
        __props__['firstTimestamp'] = first_timestamp
        __props__['lastTimestamp'] = last_timestamp
        __props__['message'] = message
        __props__['reason'] = reason
        __props__['related'] = related
        __props__['reportingComponent'] = reporting_component
        __props__['reportingInstance'] = reporting_instance
        __props__['series'] = series
        __props__['source'] = source
        __props__['type'] = type

        __props__['status'] = None

        additional_secret_outputs = [
        ]

        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(
            version=version.get_version(), additional_secret_outputs=additional_secret_outputs))

        parent = opts.parent if opts and opts.parent else None
        aliases = [
        ]

        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(
            version=version.get_version(), aliases=aliases))

        super(Event, self).__init__(
            "kubernetes:core/v1:Event",
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None):
        """
        Get the state of an existing `Event` resource, as identified by `id`.
        The ID is of the form `[namespace]/[name]`; if `[namespace]` is omitted,
        then (per Kubernetes convention) the ID becomes `default/[name]`.

        Pulumi will keep track of this resource using `resource_name` as the Pulumi ID.

        :param str resource_name: _Unique_ name used to register this resource with Pulumi.
        :param pulumi.Input[str] id: An ID for the Kubernetes resource to retrieve.
               Takes the form `[namespace]/[name]` or `[name]`.
        :param Optional[pulumi.ResourceOptions] opts: A bag of options that control this
               resource's behavior.
        """
        opts = ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))
        return Event(resource_name, opts)

    def translate_output_property(self, prop: str) -> str:
        return tables._CASING_FORWARD_TABLE.get(prop) or prop

    def translate_input_property(self, prop: str) -> str:
        return tables._CASING_BACKWARD_TABLE.get(prop) or prop
