# *** WARNING: this file was generated by the Pulumi Kubernetes codegen tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
from typing import Optional

import pulumi
import pulumi.runtime
from pulumi import Input, ResourceOptions

from ... import tables, version


class EndpointSlice(pulumi.CustomResource):
    """
    EndpointSlice represents a subset of the endpoints that implement a service. For a given service
    there may be multiple EndpointSlice objects, selected by labels, which must be joined to produce
    the full set of endpoints.
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

    address_type: pulumi.Output[str]
    """
    addressType specifies the type of address carried by this EndpointSlice. All addresses in this
    slice must be the same type. Default is IP
    """

    endpoints: pulumi.Output[list]
    """
    endpoints is a list of unique endpoints in this slice. Each slice may include a maximum of 1000
    endpoints.
    """

    metadata: pulumi.Output[dict]
    """
    Standard object's metadata.
    """

    ports: pulumi.Output[list]
    """
    ports specifies the list of network ports exposed by each endpoint in this slice. Each port must
    have a unique name. When ports is empty, it indicates that there are no defined ports. When a
    port is defined with a nil port value, it indicates "all ports". Each slice may include a
    maximum of 100 ports.
    """

    def __init__(self, resource_name, opts=None, endpoints=None, address_type=None, metadata=None, ports=None, __name__=None, __opts__=None):
        """
        Create a EndpointSlice resource with the given unique name, arguments, and options.

        :param str resource_name: The _unique_ name of the resource.
        :param pulumi.ResourceOptions opts: A bag of options that control this resource's behavior.
        :param pulumi.Input[list] endpoints: endpoints is a list of unique endpoints in this slice. Each slice may include a
               maximum of 1000 endpoints.
        :param pulumi.Input[str] address_type: addressType specifies the type of address carried by this EndpointSlice. All
               addresses in this slice must be the same type. Default is IP
        :param pulumi.Input[dict] metadata: Standard object's metadata.
        :param pulumi.Input[list] ports: ports specifies the list of network ports exposed by each endpoint in this slice.
               Each port must have a unique name. When ports is empty, it indicates that there are
               no defined ports. When a port is defined with a nil port value, it indicates "all
               ports". Each slice may include a maximum of 100 ports.
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

        __props__['apiVersion'] = 'discovery.k8s.io/v1alpha1'
        __props__['kind'] = 'EndpointSlice'
        if endpoints is None:
            raise TypeError('Missing required property endpoints')
        __props__['endpoints'] = endpoints
        __props__['addressType'] = address_type
        __props__['metadata'] = metadata
        __props__['ports'] = ports

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

        super(EndpointSlice, self).__init__(
            "kubernetes:discovery.k8s.io/v1alpha1:EndpointSlice",
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None):
        """
        Get the state of an existing `EndpointSlice` resource, as identified by `id`.
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
        return EndpointSlice(resource_name, opts)

    def translate_output_property(self, prop: str) -> str:
        return tables._CASING_FORWARD_TABLE.get(prop) or prop

    def translate_input_property(self, prop: str) -> str:
        return tables._CASING_BACKWARD_TABLE.get(prop) or prop
