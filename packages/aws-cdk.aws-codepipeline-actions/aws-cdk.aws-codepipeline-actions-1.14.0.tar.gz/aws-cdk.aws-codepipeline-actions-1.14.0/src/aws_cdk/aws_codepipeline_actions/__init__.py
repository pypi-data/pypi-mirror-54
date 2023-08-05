import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_cloudformation
import aws_cdk.aws_codebuild
import aws_cdk.aws_codecommit
import aws_cdk.aws_codedeploy
import aws_cdk.aws_codepipeline
import aws_cdk.aws_ec2
import aws_cdk.aws_ecr
import aws_cdk.aws_ecs
import aws_cdk.aws_events
import aws_cdk.aws_events_targets
import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.aws_s3
import aws_cdk.aws_sns
import aws_cdk.aws_sns_subscriptions
import aws_cdk.core
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-codepipeline-actions", "1.14.0", __name__, "aws-codepipeline-actions@1.14.0.jsii.tgz")
@jsii.implements(aws_cdk.aws_codepipeline.IAction)
class Action(metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-codepipeline-actions.Action"):
    """Low-level class for generic CodePipeline Actions.

    WARNING: this class should not be externally exposed, but is currently visible
    because of a limitation of jsii (https://github.com/aws/jsii/issues/524).

    This class will disappear in a future release and should not be used.

    stability
    :stability: experimental
    """
    @staticmethod
    def __jsii_proxy_class__():
        return _ActionProxy

    def __init__(self, *, action_name: str, artifact_bounds: aws_cdk.aws_codepipeline.ActionArtifactBounds, category: aws_cdk.aws_codepipeline.ActionCategory, provider: str, account: typing.Optional[str]=None, inputs: typing.Optional[typing.List[aws_cdk.aws_codepipeline.Artifact]]=None, outputs: typing.Optional[typing.List[aws_cdk.aws_codepipeline.Artifact]]=None, owner: typing.Optional[str]=None, region: typing.Optional[str]=None, resource: typing.Optional[aws_cdk.core.IResource]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, run_order: typing.Optional[jsii.Number]=None, version: typing.Optional[str]=None) -> None:
        """
        :param action_properties: -
        :param action_name: 
        :param artifact_bounds: 
        :param category: The category of the action. The category defines which action type the owner (the entity that performs the action) performs.
        :param provider: The service provider that the action calls.
        :param account: The account the Action is supposed to live in. For Actions backed by resources, this is inferred from the Stack {@link resource} is part of. However, some Actions, like the CloudFormation ones, are not backed by any resource, and they still might want to be cross-account. In general, a concrete Action class should specify either {@link resource}, or {@link account} - but not both.
        :param inputs: 
        :param outputs: 
        :param owner: 
        :param region: The AWS region the given Action resides in. Note that a cross-region Pipeline requires replication buckets to function correctly. You can provide their names with the {@link PipelineProps#crossRegionReplicationBuckets} property. If you don't, the CodePipeline Construct will create new Stacks in your CDK app containing those buckets, that you will need to ``cdk deploy`` before deploying the main, Pipeline-containing Stack. Default: the Action resides in the same region as the Pipeline
        :param resource: The optional resource that is backing this Action. This is used for automatically handling Actions backed by resources from a different account and/or region.
        :param role: 
        :param run_order: The order in which AWS CodePipeline runs this action. For more information, see the AWS CodePipeline User Guide. https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html#action-requirements
        :param version: 

        stability
        :stability: experimental
        """
        action_properties = aws_cdk.aws_codepipeline.ActionProperties(action_name=action_name, artifact_bounds=artifact_bounds, category=category, provider=provider, account=account, inputs=inputs, outputs=outputs, owner=owner, region=region, resource=resource, role=role, run_order=run_order, version=version)

        jsii.create(Action, self, [action_properties])

    @jsii.member(jsii_name="bind")
    def bind(self, scope: aws_cdk.core.Construct, stage: aws_cdk.aws_codepipeline.IStage, *, bucket: aws_cdk.aws_s3.IBucket, role: aws_cdk.aws_iam.IRole) -> aws_cdk.aws_codepipeline.ActionConfig:
        """
        :param scope: -
        :param stage: -
        :param options: -
        :param bucket: 
        :param role: 

        stability
        :stability: experimental
        """
        options = aws_cdk.aws_codepipeline.ActionBindOptions(bucket=bucket, role=role)

        return jsii.invoke(self, "bind", [scope, stage, options])

    @jsii.member(jsii_name="bound")
    @abc.abstractmethod
    def _bound(self, scope: aws_cdk.core.Construct, stage: aws_cdk.aws_codepipeline.IStage, *, bucket: aws_cdk.aws_s3.IBucket, role: aws_cdk.aws_iam.IRole) -> aws_cdk.aws_codepipeline.ActionConfig:
        """The method called when an Action is attached to a Pipeline. This method is guaranteed to be called only once for each Action instance.

        :param scope: -
        :param stage: -
        :param options: an instance of the {@link ActionBindOptions} class, that contains the necessary information for the Action to configure itself, like a reference to the Role, etc.
        :param bucket: 
        :param role: 

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(self, name: str, target: typing.Optional[aws_cdk.aws_events.IRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule: typing.Optional[aws_cdk.aws_events.Schedule]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IRuleTarget]]=None) -> aws_cdk.aws_events.Rule:
        """
        :param name: -
        :param target: -
        :param options: -
        :param description: A description of the rule's purpose. Default: - No description.
        :param enabled: Indicates whether the rule is enabled. Default: true
        :param event_pattern: Describes which events CloudWatch Events routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon CloudWatch User Guide. Default: - None.
        :param rule_name: A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
        :param schedule: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon CloudWatch User Guide. Default: - None.
        :param targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``. Default: - No targets.

        stability
        :stability: experimental
        """
        options = aws_cdk.aws_events.RuleProps(description=description, enabled=enabled, event_pattern=event_pattern, rule_name=rule_name, schedule=schedule, targets=targets)

        return jsii.invoke(self, "onStateChange", [name, target, options])

    @property
    @jsii.member(jsii_name="actionProperties")
    def action_properties(self) -> aws_cdk.aws_codepipeline.ActionProperties:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "actionProperties")


class _ActionProxy(Action):
    @jsii.member(jsii_name="bound")
    def _bound(self, scope: aws_cdk.core.Construct, stage: aws_cdk.aws_codepipeline.IStage, *, bucket: aws_cdk.aws_s3.IBucket, role: aws_cdk.aws_iam.IRole) -> aws_cdk.aws_codepipeline.ActionConfig:
        """The method called when an Action is attached to a Pipeline. This method is guaranteed to be called only once for each Action instance.

        :param scope: -
        :param stage: -
        :param options: an instance of the {@link ActionBindOptions} class, that contains the necessary information for the Action to configure itself, like a reference to the Role, etc.
        :param bucket: 
        :param role: 

        stability
        :stability: experimental
        """
        options = aws_cdk.aws_codepipeline.ActionBindOptions(bucket=bucket, role=role)

        return jsii.invoke(self, "bound", [scope, stage, options])


class AlexaSkillDeployAction(Action, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline-actions.AlexaSkillDeployAction"):
    """Deploys the skill to Alexa."""
    def __init__(self, *, client_id: str, client_secret: aws_cdk.core.SecretValue, input: aws_cdk.aws_codepipeline.Artifact, refresh_token: aws_cdk.core.SecretValue, skill_id: str, parameter_overrides_artifact: typing.Optional[aws_cdk.aws_codepipeline.Artifact]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None) -> None:
        """
        :param props: -
        :param client_id: The client id of the developer console token.
        :param client_secret: The client secret of the developer console token.
        :param input: The source artifact containing the voice model and skill manifest.
        :param refresh_token: The refresh token of the developer console token.
        :param skill_id: The Alexa skill id.
        :param parameter_overrides_artifact: An optional artifact containing overrides for the skill manifest.
        :param action_name: The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        """
        props = AlexaSkillDeployActionProps(client_id=client_id, client_secret=client_secret, input=input, refresh_token=refresh_token, skill_id=skill_id, parameter_overrides_artifact=parameter_overrides_artifact, action_name=action_name, run_order=run_order)

        jsii.create(AlexaSkillDeployAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(self, _scope: aws_cdk.core.Construct, _stage: aws_cdk.aws_codepipeline.IStage, *, bucket: aws_cdk.aws_s3.IBucket, role: aws_cdk.aws_iam.IRole) -> aws_cdk.aws_codepipeline.ActionConfig:
        """The method called when an Action is attached to a Pipeline. This method is guaranteed to be called only once for each Action instance.

        :param _scope: -
        :param _stage: -
        :param _options: -
        :param bucket: 
        :param role: 
        """
        _options = aws_cdk.aws_codepipeline.ActionBindOptions(bucket=bucket, role=role)

        return jsii.invoke(self, "bound", [_scope, _stage, _options])


@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-actions.AlexaSkillDeployActionProps", jsii_struct_bases=[aws_cdk.aws_codepipeline.CommonActionProps], name_mapping={'action_name': 'actionName', 'run_order': 'runOrder', 'client_id': 'clientId', 'client_secret': 'clientSecret', 'input': 'input', 'refresh_token': 'refreshToken', 'skill_id': 'skillId', 'parameter_overrides_artifact': 'parameterOverridesArtifact'})
class AlexaSkillDeployActionProps(aws_cdk.aws_codepipeline.CommonActionProps):
    def __init__(self, *, action_name: str, run_order: typing.Optional[jsii.Number]=None, client_id: str, client_secret: aws_cdk.core.SecretValue, input: aws_cdk.aws_codepipeline.Artifact, refresh_token: aws_cdk.core.SecretValue, skill_id: str, parameter_overrides_artifact: typing.Optional[aws_cdk.aws_codepipeline.Artifact]=None):
        """Construction properties of the {@link AlexaSkillDeployAction Alexa deploy Action}.

        :param action_name: The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param client_id: The client id of the developer console token.
        :param client_secret: The client secret of the developer console token.
        :param input: The source artifact containing the voice model and skill manifest.
        :param refresh_token: The refresh token of the developer console token.
        :param skill_id: The Alexa skill id.
        :param parameter_overrides_artifact: An optional artifact containing overrides for the skill manifest.
        """
        self._values = {
            'action_name': action_name,
            'client_id': client_id,
            'client_secret': client_secret,
            'input': input,
            'refresh_token': refresh_token,
            'skill_id': skill_id,
        }
        if run_order is not None: self._values["run_order"] = run_order
        if parameter_overrides_artifact is not None: self._values["parameter_overrides_artifact"] = parameter_overrides_artifact

    @property
    def action_name(self) -> str:
        """The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage."""
        return self._values.get('action_name')

    @property
    def run_order(self) -> typing.Optional[jsii.Number]:
        """The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        default
        :default: 1

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        """
        return self._values.get('run_order')

    @property
    def client_id(self) -> str:
        """The client id of the developer console token."""
        return self._values.get('client_id')

    @property
    def client_secret(self) -> aws_cdk.core.SecretValue:
        """The client secret of the developer console token."""
        return self._values.get('client_secret')

    @property
    def input(self) -> aws_cdk.aws_codepipeline.Artifact:
        """The source artifact containing the voice model and skill manifest."""
        return self._values.get('input')

    @property
    def refresh_token(self) -> aws_cdk.core.SecretValue:
        """The refresh token of the developer console token."""
        return self._values.get('refresh_token')

    @property
    def skill_id(self) -> str:
        """The Alexa skill id."""
        return self._values.get('skill_id')

    @property
    def parameter_overrides_artifact(self) -> typing.Optional[aws_cdk.aws_codepipeline.Artifact]:
        """An optional artifact containing overrides for the skill manifest."""
        return self._values.get('parameter_overrides_artifact')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'AlexaSkillDeployActionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class CloudFormationCreateReplaceChangeSetAction(Action, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline-actions.CloudFormationCreateReplaceChangeSetAction"):
    """CodePipeline action to prepare a change set.

    Creates the change set if it doesn't exist based on the stack name and template that you submit.
    If the change set exists, AWS CloudFormation deletes it, and then creates a new one.
    """
    def __init__(self, *, admin_permissions: bool, change_set_name: str, stack_name: str, template_path: aws_cdk.aws_codepipeline.ArtifactPath, account: typing.Optional[str]=None, capabilities: typing.Optional[typing.List[aws_cdk.aws_cloudformation.CloudFormationCapabilities]]=None, deployment_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, extra_inputs: typing.Optional[typing.List[aws_cdk.aws_codepipeline.Artifact]]=None, output: typing.Optional[aws_cdk.aws_codepipeline.Artifact]=None, output_file_name: typing.Optional[str]=None, parameter_overrides: typing.Optional[typing.Mapping[str,typing.Any]]=None, region: typing.Optional[str]=None, template_configuration: typing.Optional[aws_cdk.aws_codepipeline.ArtifactPath]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None) -> None:
        """
        :param props: -
        :param admin_permissions: Whether to grant full permissions to CloudFormation while deploying this template. Setting this to ``true`` affects the defaults for ``role`` and ``capabilities``, if you don't specify any alternatives. The default role that will be created for you will have full (i.e., ``*``) permissions on all resources, and the deployment will have named IAM capabilities (i.e., able to create all IAM resources). This is a shorthand that you can use if you fully trust the templates that are deployed in this pipeline. If you want more fine-grained permissions, use ``addToRolePolicy`` and ``capabilities`` to control what the CloudFormation deployment is allowed to do.
        :param change_set_name: Name of the change set to create or update.
        :param stack_name: The name of the stack to apply this action to.
        :param template_path: Input artifact with the ChangeSet's CloudFormation template.
        :param account: The AWS account this Action is supposed to operate in. **Note**: if you specify the ``role`` property, this is ignored - the action will operate in the same region the passed role does. Default: - action resides in the same account as the pipeline
        :param capabilities: Acknowledge certain changes made as part of deployment. For stacks that contain certain resources, explicit acknowledgement that AWS CloudFormation might create or update those resources. For example, you must specify ``AnonymousIAM`` or ``NamedIAM`` if your stack template contains AWS Identity and Access Management (IAM) resources. For more information see the link below. Default: None, unless ``adminPermissions`` is true
        :param deployment_role: IAM role to assume when deploying changes. If not specified, a fresh role is created. The role is created with zero permissions unless ``adminPermissions`` is true, in which case the role will have full permissions. Default: A fresh role with full or no permissions (depending on the value of ``adminPermissions``).
        :param extra_inputs: The list of additional input Artifacts for this Action. This is especially useful when used in conjunction with the ``parameterOverrides`` property. For example, if you have:. parameterOverrides: { 'Param1': action1.outputArtifact.bucketName, 'Param2': action2.outputArtifact.objectKey, } , if the output Artifacts of ``action1`` and ``action2`` were not used to set either the ``templateConfiguration`` or the ``templatePath`` properties, you need to make sure to include them in the ``extraInputs`` - otherwise, you'll get an "unrecognized Artifact" error during your Pipeline's execution.
        :param output: The name of the output artifact to generate. Only applied if ``outputFileName`` is set as well. Default: Automatically generated artifact name.
        :param output_file_name: A name for the filename in the output artifact to store the AWS CloudFormation call's result. The file will contain the result of the call to AWS CloudFormation (for example the call to UpdateStack or CreateChangeSet). AWS CodePipeline adds the file to the output artifact after performing the specified action. Default: No output artifact generated
        :param parameter_overrides: Additional template parameters. Template parameters specified here take precedence over template parameters found in the artifact specified by the ``templateConfiguration`` property. We recommend that you use the template configuration file to specify most of your parameter values. Use parameter overrides to specify only dynamic parameter values (values that are unknown until you run the pipeline). All parameter names must be present in the stack template. Note: the entire object cannot be more than 1kB. Default: No overrides
        :param region: The AWS region the given Action resides in. Note that a cross-region Pipeline requires replication buckets to function correctly. You can provide their names with the {@link PipelineProps#crossRegionReplicationBuckets} property. If you don't, the CodePipeline Construct will create new Stacks in your CDK app containing those buckets, that you will need to ``cdk deploy`` before deploying the main, Pipeline-containing Stack. Default: the Action resides in the same region as the Pipeline
        :param template_configuration: Input artifact to use for template parameters values and stack policy. The template configuration file should contain a JSON object that should look like this: ``{ "Parameters": {...}, "Tags": {...}, "StackPolicy": {... }}``. For more information, see `AWS CloudFormation Artifacts <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/continuous-delivery-codepipeline-cfn-artifacts.html>`_. Note that if you include sensitive information, such as passwords, restrict access to this file. Default: No template configuration based on input artifacts
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        """
        props = CloudFormationCreateReplaceChangeSetActionProps(admin_permissions=admin_permissions, change_set_name=change_set_name, stack_name=stack_name, template_path=template_path, account=account, capabilities=capabilities, deployment_role=deployment_role, extra_inputs=extra_inputs, output=output, output_file_name=output_file_name, parameter_overrides=parameter_overrides, region=region, template_configuration=template_configuration, role=role, action_name=action_name, run_order=run_order)

        jsii.create(CloudFormationCreateReplaceChangeSetAction, self, [props])

    @jsii.member(jsii_name="addToDeploymentRolePolicy")
    def add_to_deployment_role_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> bool:
        """Add statement to the service role assumed by CloudFormation while executing this action.

        :param statement: -
        """
        return jsii.invoke(self, "addToDeploymentRolePolicy", [statement])

    @jsii.member(jsii_name="bound")
    def _bound(self, scope: aws_cdk.core.Construct, stage: aws_cdk.aws_codepipeline.IStage, *, bucket: aws_cdk.aws_s3.IBucket, role: aws_cdk.aws_iam.IRole) -> aws_cdk.aws_codepipeline.ActionConfig:
        """The method called when an Action is attached to a Pipeline. This method is guaranteed to be called only once for each Action instance.

        :param scope: -
        :param stage: -
        :param options: -
        :param bucket: 
        :param role: 
        """
        options = aws_cdk.aws_codepipeline.ActionBindOptions(bucket=bucket, role=role)

        return jsii.invoke(self, "bound", [scope, stage, options])

    @property
    @jsii.member(jsii_name="deploymentRole")
    def deployment_role(self) -> aws_cdk.aws_iam.IRole:
        return jsii.get(self, "deploymentRole")


@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-actions.CloudFormationCreateReplaceChangeSetActionProps", jsii_struct_bases=[aws_cdk.aws_codepipeline.CommonAwsActionProps], name_mapping={'action_name': 'actionName', 'run_order': 'runOrder', 'role': 'role', 'admin_permissions': 'adminPermissions', 'change_set_name': 'changeSetName', 'stack_name': 'stackName', 'template_path': 'templatePath', 'account': 'account', 'capabilities': 'capabilities', 'deployment_role': 'deploymentRole', 'extra_inputs': 'extraInputs', 'output': 'output', 'output_file_name': 'outputFileName', 'parameter_overrides': 'parameterOverrides', 'region': 'region', 'template_configuration': 'templateConfiguration'})
class CloudFormationCreateReplaceChangeSetActionProps(aws_cdk.aws_codepipeline.CommonAwsActionProps):
    def __init__(self, *, action_name: str, run_order: typing.Optional[jsii.Number]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, admin_permissions: bool, change_set_name: str, stack_name: str, template_path: aws_cdk.aws_codepipeline.ArtifactPath, account: typing.Optional[str]=None, capabilities: typing.Optional[typing.List[aws_cdk.aws_cloudformation.CloudFormationCapabilities]]=None, deployment_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, extra_inputs: typing.Optional[typing.List[aws_cdk.aws_codepipeline.Artifact]]=None, output: typing.Optional[aws_cdk.aws_codepipeline.Artifact]=None, output_file_name: typing.Optional[str]=None, parameter_overrides: typing.Optional[typing.Mapping[str,typing.Any]]=None, region: typing.Optional[str]=None, template_configuration: typing.Optional[aws_cdk.aws_codepipeline.ArtifactPath]=None):
        """Properties for the CloudFormationCreateReplaceChangeSetAction.

        :param action_name: The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param admin_permissions: Whether to grant full permissions to CloudFormation while deploying this template. Setting this to ``true`` affects the defaults for ``role`` and ``capabilities``, if you don't specify any alternatives. The default role that will be created for you will have full (i.e., ``*``) permissions on all resources, and the deployment will have named IAM capabilities (i.e., able to create all IAM resources). This is a shorthand that you can use if you fully trust the templates that are deployed in this pipeline. If you want more fine-grained permissions, use ``addToRolePolicy`` and ``capabilities`` to control what the CloudFormation deployment is allowed to do.
        :param change_set_name: Name of the change set to create or update.
        :param stack_name: The name of the stack to apply this action to.
        :param template_path: Input artifact with the ChangeSet's CloudFormation template.
        :param account: The AWS account this Action is supposed to operate in. **Note**: if you specify the ``role`` property, this is ignored - the action will operate in the same region the passed role does. Default: - action resides in the same account as the pipeline
        :param capabilities: Acknowledge certain changes made as part of deployment. For stacks that contain certain resources, explicit acknowledgement that AWS CloudFormation might create or update those resources. For example, you must specify ``AnonymousIAM`` or ``NamedIAM`` if your stack template contains AWS Identity and Access Management (IAM) resources. For more information see the link below. Default: None, unless ``adminPermissions`` is true
        :param deployment_role: IAM role to assume when deploying changes. If not specified, a fresh role is created. The role is created with zero permissions unless ``adminPermissions`` is true, in which case the role will have full permissions. Default: A fresh role with full or no permissions (depending on the value of ``adminPermissions``).
        :param extra_inputs: The list of additional input Artifacts for this Action. This is especially useful when used in conjunction with the ``parameterOverrides`` property. For example, if you have:. parameterOverrides: { 'Param1': action1.outputArtifact.bucketName, 'Param2': action2.outputArtifact.objectKey, } , if the output Artifacts of ``action1`` and ``action2`` were not used to set either the ``templateConfiguration`` or the ``templatePath`` properties, you need to make sure to include them in the ``extraInputs`` - otherwise, you'll get an "unrecognized Artifact" error during your Pipeline's execution.
        :param output: The name of the output artifact to generate. Only applied if ``outputFileName`` is set as well. Default: Automatically generated artifact name.
        :param output_file_name: A name for the filename in the output artifact to store the AWS CloudFormation call's result. The file will contain the result of the call to AWS CloudFormation (for example the call to UpdateStack or CreateChangeSet). AWS CodePipeline adds the file to the output artifact after performing the specified action. Default: No output artifact generated
        :param parameter_overrides: Additional template parameters. Template parameters specified here take precedence over template parameters found in the artifact specified by the ``templateConfiguration`` property. We recommend that you use the template configuration file to specify most of your parameter values. Use parameter overrides to specify only dynamic parameter values (values that are unknown until you run the pipeline). All parameter names must be present in the stack template. Note: the entire object cannot be more than 1kB. Default: No overrides
        :param region: The AWS region the given Action resides in. Note that a cross-region Pipeline requires replication buckets to function correctly. You can provide their names with the {@link PipelineProps#crossRegionReplicationBuckets} property. If you don't, the CodePipeline Construct will create new Stacks in your CDK app containing those buckets, that you will need to ``cdk deploy`` before deploying the main, Pipeline-containing Stack. Default: the Action resides in the same region as the Pipeline
        :param template_configuration: Input artifact to use for template parameters values and stack policy. The template configuration file should contain a JSON object that should look like this: ``{ "Parameters": {...}, "Tags": {...}, "StackPolicy": {... }}``. For more information, see `AWS CloudFormation Artifacts <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/continuous-delivery-codepipeline-cfn-artifacts.html>`_. Note that if you include sensitive information, such as passwords, restrict access to this file. Default: No template configuration based on input artifacts
        """
        self._values = {
            'action_name': action_name,
            'admin_permissions': admin_permissions,
            'change_set_name': change_set_name,
            'stack_name': stack_name,
            'template_path': template_path,
        }
        if run_order is not None: self._values["run_order"] = run_order
        if role is not None: self._values["role"] = role
        if account is not None: self._values["account"] = account
        if capabilities is not None: self._values["capabilities"] = capabilities
        if deployment_role is not None: self._values["deployment_role"] = deployment_role
        if extra_inputs is not None: self._values["extra_inputs"] = extra_inputs
        if output is not None: self._values["output"] = output
        if output_file_name is not None: self._values["output_file_name"] = output_file_name
        if parameter_overrides is not None: self._values["parameter_overrides"] = parameter_overrides
        if region is not None: self._values["region"] = region
        if template_configuration is not None: self._values["template_configuration"] = template_configuration

    @property
    def action_name(self) -> str:
        """The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage."""
        return self._values.get('action_name')

    @property
    def run_order(self) -> typing.Optional[jsii.Number]:
        """The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        default
        :default: 1

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        """
        return self._values.get('run_order')

    @property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property.

        default
        :default: a new Role will be generated
        """
        return self._values.get('role')

    @property
    def admin_permissions(self) -> bool:
        """Whether to grant full permissions to CloudFormation while deploying this template.

        Setting this to ``true`` affects the defaults for ``role`` and ``capabilities``, if you
        don't specify any alternatives.

        The default role that will be created for you will have full (i.e., ``*``)
        permissions on all resources, and the deployment will have named IAM
        capabilities (i.e., able to create all IAM resources).

        This is a shorthand that you can use if you fully trust the templates that
        are deployed in this pipeline. If you want more fine-grained permissions,
        use ``addToRolePolicy`` and ``capabilities`` to control what the CloudFormation
        deployment is allowed to do.
        """
        return self._values.get('admin_permissions')

    @property
    def change_set_name(self) -> str:
        """Name of the change set to create or update."""
        return self._values.get('change_set_name')

    @property
    def stack_name(self) -> str:
        """The name of the stack to apply this action to."""
        return self._values.get('stack_name')

    @property
    def template_path(self) -> aws_cdk.aws_codepipeline.ArtifactPath:
        """Input artifact with the ChangeSet's CloudFormation template."""
        return self._values.get('template_path')

    @property
    def account(self) -> typing.Optional[str]:
        """The AWS account this Action is supposed to operate in. **Note**: if you specify the ``role`` property, this is ignored - the action will operate in the same region the passed role does.

        default
        :default: - action resides in the same account as the pipeline
        """
        return self._values.get('account')

    @property
    def capabilities(self) -> typing.Optional[typing.List[aws_cdk.aws_cloudformation.CloudFormationCapabilities]]:
        """Acknowledge certain changes made as part of deployment.

        For stacks that contain certain resources, explicit acknowledgement that AWS CloudFormation
        might create or update those resources. For example, you must specify ``AnonymousIAM`` or ``NamedIAM``
        if your stack template contains AWS Identity and Access Management (IAM) resources. For more
        information see the link below.

        default
        :default: None, unless ``adminPermissions`` is true

        see
        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities
        """
        return self._values.get('capabilities')

    @property
    def deployment_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """IAM role to assume when deploying changes.

        If not specified, a fresh role is created. The role is created with zero
        permissions unless ``adminPermissions`` is true, in which case the role will have
        full permissions.

        default
        :default: A fresh role with full or no permissions (depending on the value of ``adminPermissions``).
        """
        return self._values.get('deployment_role')

    @property
    def extra_inputs(self) -> typing.Optional[typing.List[aws_cdk.aws_codepipeline.Artifact]]:
        """The list of additional input Artifacts for this Action. This is especially useful when used in conjunction with the ``parameterOverrides`` property. For example, if you have:.

        parameterOverrides: {
        'Param1': action1.outputArtifact.bucketName,
        'Param2': action2.outputArtifact.objectKey,
        }

        , if the output Artifacts of ``action1`` and ``action2`` were not used to
        set either the ``templateConfiguration`` or the ``templatePath`` properties,
        you need to make sure to include them in the ``extraInputs`` -
        otherwise, you'll get an "unrecognized Artifact" error during your Pipeline's execution.
        """
        return self._values.get('extra_inputs')

    @property
    def output(self) -> typing.Optional[aws_cdk.aws_codepipeline.Artifact]:
        """The name of the output artifact to generate.

        Only applied if ``outputFileName`` is set as well.

        default
        :default: Automatically generated artifact name.
        """
        return self._values.get('output')

    @property
    def output_file_name(self) -> typing.Optional[str]:
        """A name for the filename in the output artifact to store the AWS CloudFormation call's result.

        The file will contain the result of the call to AWS CloudFormation (for example
        the call to UpdateStack or CreateChangeSet).

        AWS CodePipeline adds the file to the output artifact after performing
        the specified action.

        default
        :default: No output artifact generated
        """
        return self._values.get('output_file_name')

    @property
    def parameter_overrides(self) -> typing.Optional[typing.Mapping[str,typing.Any]]:
        """Additional template parameters.

        Template parameters specified here take precedence over template parameters
        found in the artifact specified by the ``templateConfiguration`` property.

        We recommend that you use the template configuration file to specify
        most of your parameter values. Use parameter overrides to specify only
        dynamic parameter values (values that are unknown until you run the
        pipeline).

        All parameter names must be present in the stack template.

        Note: the entire object cannot be more than 1kB.

        default
        :default: No overrides
        """
        return self._values.get('parameter_overrides')

    @property
    def region(self) -> typing.Optional[str]:
        """The AWS region the given Action resides in. Note that a cross-region Pipeline requires replication buckets to function correctly. You can provide their names with the {@link PipelineProps#crossRegionReplicationBuckets} property. If you don't, the CodePipeline Construct will create new Stacks in your CDK app containing those buckets, that you will need to ``cdk deploy`` before deploying the main, Pipeline-containing Stack.

        default
        :default: the Action resides in the same region as the Pipeline
        """
        return self._values.get('region')

    @property
    def template_configuration(self) -> typing.Optional[aws_cdk.aws_codepipeline.ArtifactPath]:
        """Input artifact to use for template parameters values and stack policy.

        The template configuration file should contain a JSON object that should look like this:
        ``{ "Parameters": {...}, "Tags": {...}, "StackPolicy": {... }}``. For more information,
        see `AWS CloudFormation Artifacts <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/continuous-delivery-codepipeline-cfn-artifacts.html>`_.

        Note that if you include sensitive information, such as passwords, restrict access to this
        file.

        default
        :default: No template configuration based on input artifacts
        """
        return self._values.get('template_configuration')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CloudFormationCreateReplaceChangeSetActionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class CloudFormationCreateUpdateStackAction(Action, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline-actions.CloudFormationCreateUpdateStackAction"):
    """CodePipeline action to deploy a stack.

    Creates the stack if the specified stack doesn't exist. If the stack exists,
    AWS CloudFormation updates the stack. Use this action to update existing
    stacks.

    AWS CodePipeline won't replace the stack, and will fail deployment if the
    stack is in a failed state. Use ``ReplaceOnFailure`` for an action that
    will delete and recreate the stack to try and recover from failed states.

    Use this action to automatically replace failed stacks without recovering or
    troubleshooting them. You would typically choose this mode for testing.
    """
    def __init__(self, *, admin_permissions: bool, stack_name: str, template_path: aws_cdk.aws_codepipeline.ArtifactPath, account: typing.Optional[str]=None, capabilities: typing.Optional[typing.List[aws_cdk.aws_cloudformation.CloudFormationCapabilities]]=None, deployment_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, extra_inputs: typing.Optional[typing.List[aws_cdk.aws_codepipeline.Artifact]]=None, output: typing.Optional[aws_cdk.aws_codepipeline.Artifact]=None, output_file_name: typing.Optional[str]=None, parameter_overrides: typing.Optional[typing.Mapping[str,typing.Any]]=None, region: typing.Optional[str]=None, replace_on_failure: typing.Optional[bool]=None, template_configuration: typing.Optional[aws_cdk.aws_codepipeline.ArtifactPath]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None) -> None:
        """
        :param props: -
        :param admin_permissions: Whether to grant full permissions to CloudFormation while deploying this template. Setting this to ``true`` affects the defaults for ``role`` and ``capabilities``, if you don't specify any alternatives. The default role that will be created for you will have full (i.e., ``*``) permissions on all resources, and the deployment will have named IAM capabilities (i.e., able to create all IAM resources). This is a shorthand that you can use if you fully trust the templates that are deployed in this pipeline. If you want more fine-grained permissions, use ``addToRolePolicy`` and ``capabilities`` to control what the CloudFormation deployment is allowed to do.
        :param stack_name: The name of the stack to apply this action to.
        :param template_path: Input artifact with the CloudFormation template to deploy.
        :param account: The AWS account this Action is supposed to operate in. **Note**: if you specify the ``role`` property, this is ignored - the action will operate in the same region the passed role does. Default: - action resides in the same account as the pipeline
        :param capabilities: Acknowledge certain changes made as part of deployment. For stacks that contain certain resources, explicit acknowledgement that AWS CloudFormation might create or update those resources. For example, you must specify ``AnonymousIAM`` or ``NamedIAM`` if your stack template contains AWS Identity and Access Management (IAM) resources. For more information see the link below. Default: None, unless ``adminPermissions`` is true
        :param deployment_role: IAM role to assume when deploying changes. If not specified, a fresh role is created. The role is created with zero permissions unless ``adminPermissions`` is true, in which case the role will have full permissions. Default: A fresh role with full or no permissions (depending on the value of ``adminPermissions``).
        :param extra_inputs: The list of additional input Artifacts for this Action. This is especially useful when used in conjunction with the ``parameterOverrides`` property. For example, if you have:. parameterOverrides: { 'Param1': action1.outputArtifact.bucketName, 'Param2': action2.outputArtifact.objectKey, } , if the output Artifacts of ``action1`` and ``action2`` were not used to set either the ``templateConfiguration`` or the ``templatePath`` properties, you need to make sure to include them in the ``extraInputs`` - otherwise, you'll get an "unrecognized Artifact" error during your Pipeline's execution.
        :param output: The name of the output artifact to generate. Only applied if ``outputFileName`` is set as well. Default: Automatically generated artifact name.
        :param output_file_name: A name for the filename in the output artifact to store the AWS CloudFormation call's result. The file will contain the result of the call to AWS CloudFormation (for example the call to UpdateStack or CreateChangeSet). AWS CodePipeline adds the file to the output artifact after performing the specified action. Default: No output artifact generated
        :param parameter_overrides: Additional template parameters. Template parameters specified here take precedence over template parameters found in the artifact specified by the ``templateConfiguration`` property. We recommend that you use the template configuration file to specify most of your parameter values. Use parameter overrides to specify only dynamic parameter values (values that are unknown until you run the pipeline). All parameter names must be present in the stack template. Note: the entire object cannot be more than 1kB. Default: No overrides
        :param region: The AWS region the given Action resides in. Note that a cross-region Pipeline requires replication buckets to function correctly. You can provide their names with the {@link PipelineProps#crossRegionReplicationBuckets} property. If you don't, the CodePipeline Construct will create new Stacks in your CDK app containing those buckets, that you will need to ``cdk deploy`` before deploying the main, Pipeline-containing Stack. Default: the Action resides in the same region as the Pipeline
        :param replace_on_failure: Replace the stack if it's in a failed state. If this is set to true and the stack is in a failed state (one of ROLLBACK_COMPLETE, ROLLBACK_FAILED, CREATE_FAILED, DELETE_FAILED, or UPDATE_ROLLBACK_FAILED), AWS CloudFormation deletes the stack and then creates a new stack. If this is not set to true and the stack is in a failed state, the deployment fails. Default: false
        :param template_configuration: Input artifact to use for template parameters values and stack policy. The template configuration file should contain a JSON object that should look like this: ``{ "Parameters": {...}, "Tags": {...}, "StackPolicy": {... }}``. For more information, see `AWS CloudFormation Artifacts <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/continuous-delivery-codepipeline-cfn-artifacts.html>`_. Note that if you include sensitive information, such as passwords, restrict access to this file. Default: No template configuration based on input artifacts
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        """
        props = CloudFormationCreateUpdateStackActionProps(admin_permissions=admin_permissions, stack_name=stack_name, template_path=template_path, account=account, capabilities=capabilities, deployment_role=deployment_role, extra_inputs=extra_inputs, output=output, output_file_name=output_file_name, parameter_overrides=parameter_overrides, region=region, replace_on_failure=replace_on_failure, template_configuration=template_configuration, role=role, action_name=action_name, run_order=run_order)

        jsii.create(CloudFormationCreateUpdateStackAction, self, [props])

    @jsii.member(jsii_name="addToDeploymentRolePolicy")
    def add_to_deployment_role_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> bool:
        """Add statement to the service role assumed by CloudFormation while executing this action.

        :param statement: -
        """
        return jsii.invoke(self, "addToDeploymentRolePolicy", [statement])

    @jsii.member(jsii_name="bound")
    def _bound(self, scope: aws_cdk.core.Construct, stage: aws_cdk.aws_codepipeline.IStage, *, bucket: aws_cdk.aws_s3.IBucket, role: aws_cdk.aws_iam.IRole) -> aws_cdk.aws_codepipeline.ActionConfig:
        """The method called when an Action is attached to a Pipeline. This method is guaranteed to be called only once for each Action instance.

        :param scope: -
        :param stage: -
        :param options: -
        :param bucket: 
        :param role: 
        """
        options = aws_cdk.aws_codepipeline.ActionBindOptions(bucket=bucket, role=role)

        return jsii.invoke(self, "bound", [scope, stage, options])

    @property
    @jsii.member(jsii_name="deploymentRole")
    def deployment_role(self) -> aws_cdk.aws_iam.IRole:
        return jsii.get(self, "deploymentRole")


@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-actions.CloudFormationCreateUpdateStackActionProps", jsii_struct_bases=[aws_cdk.aws_codepipeline.CommonAwsActionProps], name_mapping={'action_name': 'actionName', 'run_order': 'runOrder', 'role': 'role', 'admin_permissions': 'adminPermissions', 'stack_name': 'stackName', 'template_path': 'templatePath', 'account': 'account', 'capabilities': 'capabilities', 'deployment_role': 'deploymentRole', 'extra_inputs': 'extraInputs', 'output': 'output', 'output_file_name': 'outputFileName', 'parameter_overrides': 'parameterOverrides', 'region': 'region', 'replace_on_failure': 'replaceOnFailure', 'template_configuration': 'templateConfiguration'})
class CloudFormationCreateUpdateStackActionProps(aws_cdk.aws_codepipeline.CommonAwsActionProps):
    def __init__(self, *, action_name: str, run_order: typing.Optional[jsii.Number]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, admin_permissions: bool, stack_name: str, template_path: aws_cdk.aws_codepipeline.ArtifactPath, account: typing.Optional[str]=None, capabilities: typing.Optional[typing.List[aws_cdk.aws_cloudformation.CloudFormationCapabilities]]=None, deployment_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, extra_inputs: typing.Optional[typing.List[aws_cdk.aws_codepipeline.Artifact]]=None, output: typing.Optional[aws_cdk.aws_codepipeline.Artifact]=None, output_file_name: typing.Optional[str]=None, parameter_overrides: typing.Optional[typing.Mapping[str,typing.Any]]=None, region: typing.Optional[str]=None, replace_on_failure: typing.Optional[bool]=None, template_configuration: typing.Optional[aws_cdk.aws_codepipeline.ArtifactPath]=None):
        """Properties for the CloudFormationCreateUpdateStackAction.

        :param action_name: The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param admin_permissions: Whether to grant full permissions to CloudFormation while deploying this template. Setting this to ``true`` affects the defaults for ``role`` and ``capabilities``, if you don't specify any alternatives. The default role that will be created for you will have full (i.e., ``*``) permissions on all resources, and the deployment will have named IAM capabilities (i.e., able to create all IAM resources). This is a shorthand that you can use if you fully trust the templates that are deployed in this pipeline. If you want more fine-grained permissions, use ``addToRolePolicy`` and ``capabilities`` to control what the CloudFormation deployment is allowed to do.
        :param stack_name: The name of the stack to apply this action to.
        :param template_path: Input artifact with the CloudFormation template to deploy.
        :param account: The AWS account this Action is supposed to operate in. **Note**: if you specify the ``role`` property, this is ignored - the action will operate in the same region the passed role does. Default: - action resides in the same account as the pipeline
        :param capabilities: Acknowledge certain changes made as part of deployment. For stacks that contain certain resources, explicit acknowledgement that AWS CloudFormation might create or update those resources. For example, you must specify ``AnonymousIAM`` or ``NamedIAM`` if your stack template contains AWS Identity and Access Management (IAM) resources. For more information see the link below. Default: None, unless ``adminPermissions`` is true
        :param deployment_role: IAM role to assume when deploying changes. If not specified, a fresh role is created. The role is created with zero permissions unless ``adminPermissions`` is true, in which case the role will have full permissions. Default: A fresh role with full or no permissions (depending on the value of ``adminPermissions``).
        :param extra_inputs: The list of additional input Artifacts for this Action. This is especially useful when used in conjunction with the ``parameterOverrides`` property. For example, if you have:. parameterOverrides: { 'Param1': action1.outputArtifact.bucketName, 'Param2': action2.outputArtifact.objectKey, } , if the output Artifacts of ``action1`` and ``action2`` were not used to set either the ``templateConfiguration`` or the ``templatePath`` properties, you need to make sure to include them in the ``extraInputs`` - otherwise, you'll get an "unrecognized Artifact" error during your Pipeline's execution.
        :param output: The name of the output artifact to generate. Only applied if ``outputFileName`` is set as well. Default: Automatically generated artifact name.
        :param output_file_name: A name for the filename in the output artifact to store the AWS CloudFormation call's result. The file will contain the result of the call to AWS CloudFormation (for example the call to UpdateStack or CreateChangeSet). AWS CodePipeline adds the file to the output artifact after performing the specified action. Default: No output artifact generated
        :param parameter_overrides: Additional template parameters. Template parameters specified here take precedence over template parameters found in the artifact specified by the ``templateConfiguration`` property. We recommend that you use the template configuration file to specify most of your parameter values. Use parameter overrides to specify only dynamic parameter values (values that are unknown until you run the pipeline). All parameter names must be present in the stack template. Note: the entire object cannot be more than 1kB. Default: No overrides
        :param region: The AWS region the given Action resides in. Note that a cross-region Pipeline requires replication buckets to function correctly. You can provide their names with the {@link PipelineProps#crossRegionReplicationBuckets} property. If you don't, the CodePipeline Construct will create new Stacks in your CDK app containing those buckets, that you will need to ``cdk deploy`` before deploying the main, Pipeline-containing Stack. Default: the Action resides in the same region as the Pipeline
        :param replace_on_failure: Replace the stack if it's in a failed state. If this is set to true and the stack is in a failed state (one of ROLLBACK_COMPLETE, ROLLBACK_FAILED, CREATE_FAILED, DELETE_FAILED, or UPDATE_ROLLBACK_FAILED), AWS CloudFormation deletes the stack and then creates a new stack. If this is not set to true and the stack is in a failed state, the deployment fails. Default: false
        :param template_configuration: Input artifact to use for template parameters values and stack policy. The template configuration file should contain a JSON object that should look like this: ``{ "Parameters": {...}, "Tags": {...}, "StackPolicy": {... }}``. For more information, see `AWS CloudFormation Artifacts <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/continuous-delivery-codepipeline-cfn-artifacts.html>`_. Note that if you include sensitive information, such as passwords, restrict access to this file. Default: No template configuration based on input artifacts
        """
        self._values = {
            'action_name': action_name,
            'admin_permissions': admin_permissions,
            'stack_name': stack_name,
            'template_path': template_path,
        }
        if run_order is not None: self._values["run_order"] = run_order
        if role is not None: self._values["role"] = role
        if account is not None: self._values["account"] = account
        if capabilities is not None: self._values["capabilities"] = capabilities
        if deployment_role is not None: self._values["deployment_role"] = deployment_role
        if extra_inputs is not None: self._values["extra_inputs"] = extra_inputs
        if output is not None: self._values["output"] = output
        if output_file_name is not None: self._values["output_file_name"] = output_file_name
        if parameter_overrides is not None: self._values["parameter_overrides"] = parameter_overrides
        if region is not None: self._values["region"] = region
        if replace_on_failure is not None: self._values["replace_on_failure"] = replace_on_failure
        if template_configuration is not None: self._values["template_configuration"] = template_configuration

    @property
    def action_name(self) -> str:
        """The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage."""
        return self._values.get('action_name')

    @property
    def run_order(self) -> typing.Optional[jsii.Number]:
        """The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        default
        :default: 1

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        """
        return self._values.get('run_order')

    @property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property.

        default
        :default: a new Role will be generated
        """
        return self._values.get('role')

    @property
    def admin_permissions(self) -> bool:
        """Whether to grant full permissions to CloudFormation while deploying this template.

        Setting this to ``true`` affects the defaults for ``role`` and ``capabilities``, if you
        don't specify any alternatives.

        The default role that will be created for you will have full (i.e., ``*``)
        permissions on all resources, and the deployment will have named IAM
        capabilities (i.e., able to create all IAM resources).

        This is a shorthand that you can use if you fully trust the templates that
        are deployed in this pipeline. If you want more fine-grained permissions,
        use ``addToRolePolicy`` and ``capabilities`` to control what the CloudFormation
        deployment is allowed to do.
        """
        return self._values.get('admin_permissions')

    @property
    def stack_name(self) -> str:
        """The name of the stack to apply this action to."""
        return self._values.get('stack_name')

    @property
    def template_path(self) -> aws_cdk.aws_codepipeline.ArtifactPath:
        """Input artifact with the CloudFormation template to deploy."""
        return self._values.get('template_path')

    @property
    def account(self) -> typing.Optional[str]:
        """The AWS account this Action is supposed to operate in. **Note**: if you specify the ``role`` property, this is ignored - the action will operate in the same region the passed role does.

        default
        :default: - action resides in the same account as the pipeline
        """
        return self._values.get('account')

    @property
    def capabilities(self) -> typing.Optional[typing.List[aws_cdk.aws_cloudformation.CloudFormationCapabilities]]:
        """Acknowledge certain changes made as part of deployment.

        For stacks that contain certain resources, explicit acknowledgement that AWS CloudFormation
        might create or update those resources. For example, you must specify ``AnonymousIAM`` or ``NamedIAM``
        if your stack template contains AWS Identity and Access Management (IAM) resources. For more
        information see the link below.

        default
        :default: None, unless ``adminPermissions`` is true

        see
        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities
        """
        return self._values.get('capabilities')

    @property
    def deployment_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """IAM role to assume when deploying changes.

        If not specified, a fresh role is created. The role is created with zero
        permissions unless ``adminPermissions`` is true, in which case the role will have
        full permissions.

        default
        :default: A fresh role with full or no permissions (depending on the value of ``adminPermissions``).
        """
        return self._values.get('deployment_role')

    @property
    def extra_inputs(self) -> typing.Optional[typing.List[aws_cdk.aws_codepipeline.Artifact]]:
        """The list of additional input Artifacts for this Action. This is especially useful when used in conjunction with the ``parameterOverrides`` property. For example, if you have:.

        parameterOverrides: {
        'Param1': action1.outputArtifact.bucketName,
        'Param2': action2.outputArtifact.objectKey,
        }

        , if the output Artifacts of ``action1`` and ``action2`` were not used to
        set either the ``templateConfiguration`` or the ``templatePath`` properties,
        you need to make sure to include them in the ``extraInputs`` -
        otherwise, you'll get an "unrecognized Artifact" error during your Pipeline's execution.
        """
        return self._values.get('extra_inputs')

    @property
    def output(self) -> typing.Optional[aws_cdk.aws_codepipeline.Artifact]:
        """The name of the output artifact to generate.

        Only applied if ``outputFileName`` is set as well.

        default
        :default: Automatically generated artifact name.
        """
        return self._values.get('output')

    @property
    def output_file_name(self) -> typing.Optional[str]:
        """A name for the filename in the output artifact to store the AWS CloudFormation call's result.

        The file will contain the result of the call to AWS CloudFormation (for example
        the call to UpdateStack or CreateChangeSet).

        AWS CodePipeline adds the file to the output artifact after performing
        the specified action.

        default
        :default: No output artifact generated
        """
        return self._values.get('output_file_name')

    @property
    def parameter_overrides(self) -> typing.Optional[typing.Mapping[str,typing.Any]]:
        """Additional template parameters.

        Template parameters specified here take precedence over template parameters
        found in the artifact specified by the ``templateConfiguration`` property.

        We recommend that you use the template configuration file to specify
        most of your parameter values. Use parameter overrides to specify only
        dynamic parameter values (values that are unknown until you run the
        pipeline).

        All parameter names must be present in the stack template.

        Note: the entire object cannot be more than 1kB.

        default
        :default: No overrides
        """
        return self._values.get('parameter_overrides')

    @property
    def region(self) -> typing.Optional[str]:
        """The AWS region the given Action resides in. Note that a cross-region Pipeline requires replication buckets to function correctly. You can provide their names with the {@link PipelineProps#crossRegionReplicationBuckets} property. If you don't, the CodePipeline Construct will create new Stacks in your CDK app containing those buckets, that you will need to ``cdk deploy`` before deploying the main, Pipeline-containing Stack.

        default
        :default: the Action resides in the same region as the Pipeline
        """
        return self._values.get('region')

    @property
    def replace_on_failure(self) -> typing.Optional[bool]:
        """Replace the stack if it's in a failed state.

        If this is set to true and the stack is in a failed state (one of
        ROLLBACK_COMPLETE, ROLLBACK_FAILED, CREATE_FAILED, DELETE_FAILED, or
        UPDATE_ROLLBACK_FAILED), AWS CloudFormation deletes the stack and then
        creates a new stack.

        If this is not set to true and the stack is in a failed state,
        the deployment fails.

        default
        :default: false
        """
        return self._values.get('replace_on_failure')

    @property
    def template_configuration(self) -> typing.Optional[aws_cdk.aws_codepipeline.ArtifactPath]:
        """Input artifact to use for template parameters values and stack policy.

        The template configuration file should contain a JSON object that should look like this:
        ``{ "Parameters": {...}, "Tags": {...}, "StackPolicy": {... }}``. For more information,
        see `AWS CloudFormation Artifacts <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/continuous-delivery-codepipeline-cfn-artifacts.html>`_.

        Note that if you include sensitive information, such as passwords, restrict access to this
        file.

        default
        :default: No template configuration based on input artifacts
        """
        return self._values.get('template_configuration')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CloudFormationCreateUpdateStackActionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class CloudFormationDeleteStackAction(Action, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline-actions.CloudFormationDeleteStackAction"):
    """CodePipeline action to delete a stack.

    Deletes a stack. If you specify a stack that doesn't exist, the action completes successfully
    without deleting a stack.
    """
    def __init__(self, *, admin_permissions: bool, stack_name: str, account: typing.Optional[str]=None, capabilities: typing.Optional[typing.List[aws_cdk.aws_cloudformation.CloudFormationCapabilities]]=None, deployment_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, extra_inputs: typing.Optional[typing.List[aws_cdk.aws_codepipeline.Artifact]]=None, output: typing.Optional[aws_cdk.aws_codepipeline.Artifact]=None, output_file_name: typing.Optional[str]=None, parameter_overrides: typing.Optional[typing.Mapping[str,typing.Any]]=None, region: typing.Optional[str]=None, template_configuration: typing.Optional[aws_cdk.aws_codepipeline.ArtifactPath]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None) -> None:
        """
        :param props: -
        :param admin_permissions: Whether to grant full permissions to CloudFormation while deploying this template. Setting this to ``true`` affects the defaults for ``role`` and ``capabilities``, if you don't specify any alternatives. The default role that will be created for you will have full (i.e., ``*``) permissions on all resources, and the deployment will have named IAM capabilities (i.e., able to create all IAM resources). This is a shorthand that you can use if you fully trust the templates that are deployed in this pipeline. If you want more fine-grained permissions, use ``addToRolePolicy`` and ``capabilities`` to control what the CloudFormation deployment is allowed to do.
        :param stack_name: The name of the stack to apply this action to.
        :param account: The AWS account this Action is supposed to operate in. **Note**: if you specify the ``role`` property, this is ignored - the action will operate in the same region the passed role does. Default: - action resides in the same account as the pipeline
        :param capabilities: Acknowledge certain changes made as part of deployment. For stacks that contain certain resources, explicit acknowledgement that AWS CloudFormation might create or update those resources. For example, you must specify ``AnonymousIAM`` or ``NamedIAM`` if your stack template contains AWS Identity and Access Management (IAM) resources. For more information see the link below. Default: None, unless ``adminPermissions`` is true
        :param deployment_role: IAM role to assume when deploying changes. If not specified, a fresh role is created. The role is created with zero permissions unless ``adminPermissions`` is true, in which case the role will have full permissions. Default: A fresh role with full or no permissions (depending on the value of ``adminPermissions``).
        :param extra_inputs: The list of additional input Artifacts for this Action. This is especially useful when used in conjunction with the ``parameterOverrides`` property. For example, if you have:. parameterOverrides: { 'Param1': action1.outputArtifact.bucketName, 'Param2': action2.outputArtifact.objectKey, } , if the output Artifacts of ``action1`` and ``action2`` were not used to set either the ``templateConfiguration`` or the ``templatePath`` properties, you need to make sure to include them in the ``extraInputs`` - otherwise, you'll get an "unrecognized Artifact" error during your Pipeline's execution.
        :param output: The name of the output artifact to generate. Only applied if ``outputFileName`` is set as well. Default: Automatically generated artifact name.
        :param output_file_name: A name for the filename in the output artifact to store the AWS CloudFormation call's result. The file will contain the result of the call to AWS CloudFormation (for example the call to UpdateStack or CreateChangeSet). AWS CodePipeline adds the file to the output artifact after performing the specified action. Default: No output artifact generated
        :param parameter_overrides: Additional template parameters. Template parameters specified here take precedence over template parameters found in the artifact specified by the ``templateConfiguration`` property. We recommend that you use the template configuration file to specify most of your parameter values. Use parameter overrides to specify only dynamic parameter values (values that are unknown until you run the pipeline). All parameter names must be present in the stack template. Note: the entire object cannot be more than 1kB. Default: No overrides
        :param region: The AWS region the given Action resides in. Note that a cross-region Pipeline requires replication buckets to function correctly. You can provide their names with the {@link PipelineProps#crossRegionReplicationBuckets} property. If you don't, the CodePipeline Construct will create new Stacks in your CDK app containing those buckets, that you will need to ``cdk deploy`` before deploying the main, Pipeline-containing Stack. Default: the Action resides in the same region as the Pipeline
        :param template_configuration: Input artifact to use for template parameters values and stack policy. The template configuration file should contain a JSON object that should look like this: ``{ "Parameters": {...}, "Tags": {...}, "StackPolicy": {... }}``. For more information, see `AWS CloudFormation Artifacts <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/continuous-delivery-codepipeline-cfn-artifacts.html>`_. Note that if you include sensitive information, such as passwords, restrict access to this file. Default: No template configuration based on input artifacts
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        """
        props = CloudFormationDeleteStackActionProps(admin_permissions=admin_permissions, stack_name=stack_name, account=account, capabilities=capabilities, deployment_role=deployment_role, extra_inputs=extra_inputs, output=output, output_file_name=output_file_name, parameter_overrides=parameter_overrides, region=region, template_configuration=template_configuration, role=role, action_name=action_name, run_order=run_order)

        jsii.create(CloudFormationDeleteStackAction, self, [props])

    @jsii.member(jsii_name="addToDeploymentRolePolicy")
    def add_to_deployment_role_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> bool:
        """Add statement to the service role assumed by CloudFormation while executing this action.

        :param statement: -
        """
        return jsii.invoke(self, "addToDeploymentRolePolicy", [statement])

    @jsii.member(jsii_name="bound")
    def _bound(self, scope: aws_cdk.core.Construct, stage: aws_cdk.aws_codepipeline.IStage, *, bucket: aws_cdk.aws_s3.IBucket, role: aws_cdk.aws_iam.IRole) -> aws_cdk.aws_codepipeline.ActionConfig:
        """The method called when an Action is attached to a Pipeline. This method is guaranteed to be called only once for each Action instance.

        :param scope: -
        :param stage: -
        :param options: -
        :param bucket: 
        :param role: 
        """
        options = aws_cdk.aws_codepipeline.ActionBindOptions(bucket=bucket, role=role)

        return jsii.invoke(self, "bound", [scope, stage, options])

    @property
    @jsii.member(jsii_name="deploymentRole")
    def deployment_role(self) -> aws_cdk.aws_iam.IRole:
        return jsii.get(self, "deploymentRole")


@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-actions.CloudFormationDeleteStackActionProps", jsii_struct_bases=[aws_cdk.aws_codepipeline.CommonAwsActionProps], name_mapping={'action_name': 'actionName', 'run_order': 'runOrder', 'role': 'role', 'admin_permissions': 'adminPermissions', 'stack_name': 'stackName', 'account': 'account', 'capabilities': 'capabilities', 'deployment_role': 'deploymentRole', 'extra_inputs': 'extraInputs', 'output': 'output', 'output_file_name': 'outputFileName', 'parameter_overrides': 'parameterOverrides', 'region': 'region', 'template_configuration': 'templateConfiguration'})
class CloudFormationDeleteStackActionProps(aws_cdk.aws_codepipeline.CommonAwsActionProps):
    def __init__(self, *, action_name: str, run_order: typing.Optional[jsii.Number]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, admin_permissions: bool, stack_name: str, account: typing.Optional[str]=None, capabilities: typing.Optional[typing.List[aws_cdk.aws_cloudformation.CloudFormationCapabilities]]=None, deployment_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, extra_inputs: typing.Optional[typing.List[aws_cdk.aws_codepipeline.Artifact]]=None, output: typing.Optional[aws_cdk.aws_codepipeline.Artifact]=None, output_file_name: typing.Optional[str]=None, parameter_overrides: typing.Optional[typing.Mapping[str,typing.Any]]=None, region: typing.Optional[str]=None, template_configuration: typing.Optional[aws_cdk.aws_codepipeline.ArtifactPath]=None):
        """Properties for the CloudFormationDeleteStackAction.

        :param action_name: The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param admin_permissions: Whether to grant full permissions to CloudFormation while deploying this template. Setting this to ``true`` affects the defaults for ``role`` and ``capabilities``, if you don't specify any alternatives. The default role that will be created for you will have full (i.e., ``*``) permissions on all resources, and the deployment will have named IAM capabilities (i.e., able to create all IAM resources). This is a shorthand that you can use if you fully trust the templates that are deployed in this pipeline. If you want more fine-grained permissions, use ``addToRolePolicy`` and ``capabilities`` to control what the CloudFormation deployment is allowed to do.
        :param stack_name: The name of the stack to apply this action to.
        :param account: The AWS account this Action is supposed to operate in. **Note**: if you specify the ``role`` property, this is ignored - the action will operate in the same region the passed role does. Default: - action resides in the same account as the pipeline
        :param capabilities: Acknowledge certain changes made as part of deployment. For stacks that contain certain resources, explicit acknowledgement that AWS CloudFormation might create or update those resources. For example, you must specify ``AnonymousIAM`` or ``NamedIAM`` if your stack template contains AWS Identity and Access Management (IAM) resources. For more information see the link below. Default: None, unless ``adminPermissions`` is true
        :param deployment_role: IAM role to assume when deploying changes. If not specified, a fresh role is created. The role is created with zero permissions unless ``adminPermissions`` is true, in which case the role will have full permissions. Default: A fresh role with full or no permissions (depending on the value of ``adminPermissions``).
        :param extra_inputs: The list of additional input Artifacts for this Action. This is especially useful when used in conjunction with the ``parameterOverrides`` property. For example, if you have:. parameterOverrides: { 'Param1': action1.outputArtifact.bucketName, 'Param2': action2.outputArtifact.objectKey, } , if the output Artifacts of ``action1`` and ``action2`` were not used to set either the ``templateConfiguration`` or the ``templatePath`` properties, you need to make sure to include them in the ``extraInputs`` - otherwise, you'll get an "unrecognized Artifact" error during your Pipeline's execution.
        :param output: The name of the output artifact to generate. Only applied if ``outputFileName`` is set as well. Default: Automatically generated artifact name.
        :param output_file_name: A name for the filename in the output artifact to store the AWS CloudFormation call's result. The file will contain the result of the call to AWS CloudFormation (for example the call to UpdateStack or CreateChangeSet). AWS CodePipeline adds the file to the output artifact after performing the specified action. Default: No output artifact generated
        :param parameter_overrides: Additional template parameters. Template parameters specified here take precedence over template parameters found in the artifact specified by the ``templateConfiguration`` property. We recommend that you use the template configuration file to specify most of your parameter values. Use parameter overrides to specify only dynamic parameter values (values that are unknown until you run the pipeline). All parameter names must be present in the stack template. Note: the entire object cannot be more than 1kB. Default: No overrides
        :param region: The AWS region the given Action resides in. Note that a cross-region Pipeline requires replication buckets to function correctly. You can provide their names with the {@link PipelineProps#crossRegionReplicationBuckets} property. If you don't, the CodePipeline Construct will create new Stacks in your CDK app containing those buckets, that you will need to ``cdk deploy`` before deploying the main, Pipeline-containing Stack. Default: the Action resides in the same region as the Pipeline
        :param template_configuration: Input artifact to use for template parameters values and stack policy. The template configuration file should contain a JSON object that should look like this: ``{ "Parameters": {...}, "Tags": {...}, "StackPolicy": {... }}``. For more information, see `AWS CloudFormation Artifacts <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/continuous-delivery-codepipeline-cfn-artifacts.html>`_. Note that if you include sensitive information, such as passwords, restrict access to this file. Default: No template configuration based on input artifacts
        """
        self._values = {
            'action_name': action_name,
            'admin_permissions': admin_permissions,
            'stack_name': stack_name,
        }
        if run_order is not None: self._values["run_order"] = run_order
        if role is not None: self._values["role"] = role
        if account is not None: self._values["account"] = account
        if capabilities is not None: self._values["capabilities"] = capabilities
        if deployment_role is not None: self._values["deployment_role"] = deployment_role
        if extra_inputs is not None: self._values["extra_inputs"] = extra_inputs
        if output is not None: self._values["output"] = output
        if output_file_name is not None: self._values["output_file_name"] = output_file_name
        if parameter_overrides is not None: self._values["parameter_overrides"] = parameter_overrides
        if region is not None: self._values["region"] = region
        if template_configuration is not None: self._values["template_configuration"] = template_configuration

    @property
    def action_name(self) -> str:
        """The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage."""
        return self._values.get('action_name')

    @property
    def run_order(self) -> typing.Optional[jsii.Number]:
        """The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        default
        :default: 1

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        """
        return self._values.get('run_order')

    @property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property.

        default
        :default: a new Role will be generated
        """
        return self._values.get('role')

    @property
    def admin_permissions(self) -> bool:
        """Whether to grant full permissions to CloudFormation while deploying this template.

        Setting this to ``true`` affects the defaults for ``role`` and ``capabilities``, if you
        don't specify any alternatives.

        The default role that will be created for you will have full (i.e., ``*``)
        permissions on all resources, and the deployment will have named IAM
        capabilities (i.e., able to create all IAM resources).

        This is a shorthand that you can use if you fully trust the templates that
        are deployed in this pipeline. If you want more fine-grained permissions,
        use ``addToRolePolicy`` and ``capabilities`` to control what the CloudFormation
        deployment is allowed to do.
        """
        return self._values.get('admin_permissions')

    @property
    def stack_name(self) -> str:
        """The name of the stack to apply this action to."""
        return self._values.get('stack_name')

    @property
    def account(self) -> typing.Optional[str]:
        """The AWS account this Action is supposed to operate in. **Note**: if you specify the ``role`` property, this is ignored - the action will operate in the same region the passed role does.

        default
        :default: - action resides in the same account as the pipeline
        """
        return self._values.get('account')

    @property
    def capabilities(self) -> typing.Optional[typing.List[aws_cdk.aws_cloudformation.CloudFormationCapabilities]]:
        """Acknowledge certain changes made as part of deployment.

        For stacks that contain certain resources, explicit acknowledgement that AWS CloudFormation
        might create or update those resources. For example, you must specify ``AnonymousIAM`` or ``NamedIAM``
        if your stack template contains AWS Identity and Access Management (IAM) resources. For more
        information see the link below.

        default
        :default: None, unless ``adminPermissions`` is true

        see
        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities
        """
        return self._values.get('capabilities')

    @property
    def deployment_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """IAM role to assume when deploying changes.

        If not specified, a fresh role is created. The role is created with zero
        permissions unless ``adminPermissions`` is true, in which case the role will have
        full permissions.

        default
        :default: A fresh role with full or no permissions (depending on the value of ``adminPermissions``).
        """
        return self._values.get('deployment_role')

    @property
    def extra_inputs(self) -> typing.Optional[typing.List[aws_cdk.aws_codepipeline.Artifact]]:
        """The list of additional input Artifacts for this Action. This is especially useful when used in conjunction with the ``parameterOverrides`` property. For example, if you have:.

        parameterOverrides: {
        'Param1': action1.outputArtifact.bucketName,
        'Param2': action2.outputArtifact.objectKey,
        }

        , if the output Artifacts of ``action1`` and ``action2`` were not used to
        set either the ``templateConfiguration`` or the ``templatePath`` properties,
        you need to make sure to include them in the ``extraInputs`` -
        otherwise, you'll get an "unrecognized Artifact" error during your Pipeline's execution.
        """
        return self._values.get('extra_inputs')

    @property
    def output(self) -> typing.Optional[aws_cdk.aws_codepipeline.Artifact]:
        """The name of the output artifact to generate.

        Only applied if ``outputFileName`` is set as well.

        default
        :default: Automatically generated artifact name.
        """
        return self._values.get('output')

    @property
    def output_file_name(self) -> typing.Optional[str]:
        """A name for the filename in the output artifact to store the AWS CloudFormation call's result.

        The file will contain the result of the call to AWS CloudFormation (for example
        the call to UpdateStack or CreateChangeSet).

        AWS CodePipeline adds the file to the output artifact after performing
        the specified action.

        default
        :default: No output artifact generated
        """
        return self._values.get('output_file_name')

    @property
    def parameter_overrides(self) -> typing.Optional[typing.Mapping[str,typing.Any]]:
        """Additional template parameters.

        Template parameters specified here take precedence over template parameters
        found in the artifact specified by the ``templateConfiguration`` property.

        We recommend that you use the template configuration file to specify
        most of your parameter values. Use parameter overrides to specify only
        dynamic parameter values (values that are unknown until you run the
        pipeline).

        All parameter names must be present in the stack template.

        Note: the entire object cannot be more than 1kB.

        default
        :default: No overrides
        """
        return self._values.get('parameter_overrides')

    @property
    def region(self) -> typing.Optional[str]:
        """The AWS region the given Action resides in. Note that a cross-region Pipeline requires replication buckets to function correctly. You can provide their names with the {@link PipelineProps#crossRegionReplicationBuckets} property. If you don't, the CodePipeline Construct will create new Stacks in your CDK app containing those buckets, that you will need to ``cdk deploy`` before deploying the main, Pipeline-containing Stack.

        default
        :default: the Action resides in the same region as the Pipeline
        """
        return self._values.get('region')

    @property
    def template_configuration(self) -> typing.Optional[aws_cdk.aws_codepipeline.ArtifactPath]:
        """Input artifact to use for template parameters values and stack policy.

        The template configuration file should contain a JSON object that should look like this:
        ``{ "Parameters": {...}, "Tags": {...}, "StackPolicy": {... }}``. For more information,
        see `AWS CloudFormation Artifacts <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/continuous-delivery-codepipeline-cfn-artifacts.html>`_.

        Note that if you include sensitive information, such as passwords, restrict access to this
        file.

        default
        :default: No template configuration based on input artifacts
        """
        return self._values.get('template_configuration')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CloudFormationDeleteStackActionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class CloudFormationExecuteChangeSetAction(Action, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline-actions.CloudFormationExecuteChangeSetAction"):
    """CodePipeline action to execute a prepared change set."""
    def __init__(self, *, change_set_name: str, stack_name: str, account: typing.Optional[str]=None, output: typing.Optional[aws_cdk.aws_codepipeline.Artifact]=None, output_file_name: typing.Optional[str]=None, region: typing.Optional[str]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None) -> None:
        """
        :param props: -
        :param change_set_name: Name of the change set to execute.
        :param stack_name: The name of the stack to apply this action to.
        :param account: The AWS account this Action is supposed to operate in. **Note**: if you specify the ``role`` property, this is ignored - the action will operate in the same region the passed role does. Default: - action resides in the same account as the pipeline
        :param output: The name of the output artifact to generate. Only applied if ``outputFileName`` is set as well. Default: Automatically generated artifact name.
        :param output_file_name: A name for the filename in the output artifact to store the AWS CloudFormation call's result. The file will contain the result of the call to AWS CloudFormation (for example the call to UpdateStack or CreateChangeSet). AWS CodePipeline adds the file to the output artifact after performing the specified action. Default: No output artifact generated
        :param region: The AWS region the given Action resides in. Note that a cross-region Pipeline requires replication buckets to function correctly. You can provide their names with the {@link PipelineProps#crossRegionReplicationBuckets} property. If you don't, the CodePipeline Construct will create new Stacks in your CDK app containing those buckets, that you will need to ``cdk deploy`` before deploying the main, Pipeline-containing Stack. Default: the Action resides in the same region as the Pipeline
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        """
        props = CloudFormationExecuteChangeSetActionProps(change_set_name=change_set_name, stack_name=stack_name, account=account, output=output, output_file_name=output_file_name, region=region, role=role, action_name=action_name, run_order=run_order)

        jsii.create(CloudFormationExecuteChangeSetAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(self, scope: aws_cdk.core.Construct, stage: aws_cdk.aws_codepipeline.IStage, *, bucket: aws_cdk.aws_s3.IBucket, role: aws_cdk.aws_iam.IRole) -> aws_cdk.aws_codepipeline.ActionConfig:
        """The method called when an Action is attached to a Pipeline. This method is guaranteed to be called only once for each Action instance.

        :param scope: -
        :param stage: -
        :param options: -
        :param bucket: 
        :param role: 
        """
        options = aws_cdk.aws_codepipeline.ActionBindOptions(bucket=bucket, role=role)

        return jsii.invoke(self, "bound", [scope, stage, options])


@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-actions.CloudFormationExecuteChangeSetActionProps", jsii_struct_bases=[aws_cdk.aws_codepipeline.CommonAwsActionProps], name_mapping={'action_name': 'actionName', 'run_order': 'runOrder', 'role': 'role', 'change_set_name': 'changeSetName', 'stack_name': 'stackName', 'account': 'account', 'output': 'output', 'output_file_name': 'outputFileName', 'region': 'region'})
class CloudFormationExecuteChangeSetActionProps(aws_cdk.aws_codepipeline.CommonAwsActionProps):
    def __init__(self, *, action_name: str, run_order: typing.Optional[jsii.Number]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, change_set_name: str, stack_name: str, account: typing.Optional[str]=None, output: typing.Optional[aws_cdk.aws_codepipeline.Artifact]=None, output_file_name: typing.Optional[str]=None, region: typing.Optional[str]=None):
        """Properties for the CloudFormationExecuteChangeSetAction.

        :param action_name: The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param change_set_name: Name of the change set to execute.
        :param stack_name: The name of the stack to apply this action to.
        :param account: The AWS account this Action is supposed to operate in. **Note**: if you specify the ``role`` property, this is ignored - the action will operate in the same region the passed role does. Default: - action resides in the same account as the pipeline
        :param output: The name of the output artifact to generate. Only applied if ``outputFileName`` is set as well. Default: Automatically generated artifact name.
        :param output_file_name: A name for the filename in the output artifact to store the AWS CloudFormation call's result. The file will contain the result of the call to AWS CloudFormation (for example the call to UpdateStack or CreateChangeSet). AWS CodePipeline adds the file to the output artifact after performing the specified action. Default: No output artifact generated
        :param region: The AWS region the given Action resides in. Note that a cross-region Pipeline requires replication buckets to function correctly. You can provide their names with the {@link PipelineProps#crossRegionReplicationBuckets} property. If you don't, the CodePipeline Construct will create new Stacks in your CDK app containing those buckets, that you will need to ``cdk deploy`` before deploying the main, Pipeline-containing Stack. Default: the Action resides in the same region as the Pipeline
        """
        self._values = {
            'action_name': action_name,
            'change_set_name': change_set_name,
            'stack_name': stack_name,
        }
        if run_order is not None: self._values["run_order"] = run_order
        if role is not None: self._values["role"] = role
        if account is not None: self._values["account"] = account
        if output is not None: self._values["output"] = output
        if output_file_name is not None: self._values["output_file_name"] = output_file_name
        if region is not None: self._values["region"] = region

    @property
    def action_name(self) -> str:
        """The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage."""
        return self._values.get('action_name')

    @property
    def run_order(self) -> typing.Optional[jsii.Number]:
        """The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        default
        :default: 1

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        """
        return self._values.get('run_order')

    @property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property.

        default
        :default: a new Role will be generated
        """
        return self._values.get('role')

    @property
    def change_set_name(self) -> str:
        """Name of the change set to execute."""
        return self._values.get('change_set_name')

    @property
    def stack_name(self) -> str:
        """The name of the stack to apply this action to."""
        return self._values.get('stack_name')

    @property
    def account(self) -> typing.Optional[str]:
        """The AWS account this Action is supposed to operate in. **Note**: if you specify the ``role`` property, this is ignored - the action will operate in the same region the passed role does.

        default
        :default: - action resides in the same account as the pipeline
        """
        return self._values.get('account')

    @property
    def output(self) -> typing.Optional[aws_cdk.aws_codepipeline.Artifact]:
        """The name of the output artifact to generate.

        Only applied if ``outputFileName`` is set as well.

        default
        :default: Automatically generated artifact name.
        """
        return self._values.get('output')

    @property
    def output_file_name(self) -> typing.Optional[str]:
        """A name for the filename in the output artifact to store the AWS CloudFormation call's result.

        The file will contain the result of the call to AWS CloudFormation (for example
        the call to UpdateStack or CreateChangeSet).

        AWS CodePipeline adds the file to the output artifact after performing
        the specified action.

        default
        :default: No output artifact generated
        """
        return self._values.get('output_file_name')

    @property
    def region(self) -> typing.Optional[str]:
        """The AWS region the given Action resides in. Note that a cross-region Pipeline requires replication buckets to function correctly. You can provide their names with the {@link PipelineProps#crossRegionReplicationBuckets} property. If you don't, the CodePipeline Construct will create new Stacks in your CDK app containing those buckets, that you will need to ``cdk deploy`` before deploying the main, Pipeline-containing Stack.

        default
        :default: the Action resides in the same region as the Pipeline
        """
        return self._values.get('region')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CloudFormationExecuteChangeSetActionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class CodeBuildAction(Action, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline-actions.CodeBuildAction"):
    """CodePipeline build action that uses AWS CodeBuild."""
    def __init__(self, *, input: aws_cdk.aws_codepipeline.Artifact, project: aws_cdk.aws_codebuild.IProject, extra_inputs: typing.Optional[typing.List[aws_cdk.aws_codepipeline.Artifact]]=None, outputs: typing.Optional[typing.List[aws_cdk.aws_codepipeline.Artifact]]=None, type: typing.Optional["CodeBuildActionType"]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None) -> None:
        """
        :param props: -
        :param input: The source to use as input for this action.
        :param project: The action's Project.
        :param extra_inputs: The list of additional input Artifacts for this action.
        :param outputs: The list of output Artifacts for this action. **Note**: if you specify more than one output Artifact here, you cannot use the primary 'artifacts' section of the buildspec; you have to use the 'secondary-artifacts' section instead. See https://docs.aws.amazon.com/codebuild/latest/userguide/sample-multi-in-out.html for details. Default: the action will not have any outputs
        :param type: The type of the action that determines its CodePipeline Category - Build, or Test. Default: CodeBuildActionType.BUILD
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        """
        props = CodeBuildActionProps(input=input, project=project, extra_inputs=extra_inputs, outputs=outputs, type=type, role=role, action_name=action_name, run_order=run_order)

        jsii.create(CodeBuildAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(self, scope: aws_cdk.core.Construct, _stage: aws_cdk.aws_codepipeline.IStage, *, bucket: aws_cdk.aws_s3.IBucket, role: aws_cdk.aws_iam.IRole) -> aws_cdk.aws_codepipeline.ActionConfig:
        """The method called when an Action is attached to a Pipeline. This method is guaranteed to be called only once for each Action instance.

        :param scope: -
        :param _stage: -
        :param options: -
        :param bucket: 
        :param role: 
        """
        options = aws_cdk.aws_codepipeline.ActionBindOptions(bucket=bucket, role=role)

        return jsii.invoke(self, "bound", [scope, _stage, options])


@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-actions.CodeBuildActionProps", jsii_struct_bases=[aws_cdk.aws_codepipeline.CommonAwsActionProps], name_mapping={'action_name': 'actionName', 'run_order': 'runOrder', 'role': 'role', 'input': 'input', 'project': 'project', 'extra_inputs': 'extraInputs', 'outputs': 'outputs', 'type': 'type'})
class CodeBuildActionProps(aws_cdk.aws_codepipeline.CommonAwsActionProps):
    def __init__(self, *, action_name: str, run_order: typing.Optional[jsii.Number]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, input: aws_cdk.aws_codepipeline.Artifact, project: aws_cdk.aws_codebuild.IProject, extra_inputs: typing.Optional[typing.List[aws_cdk.aws_codepipeline.Artifact]]=None, outputs: typing.Optional[typing.List[aws_cdk.aws_codepipeline.Artifact]]=None, type: typing.Optional["CodeBuildActionType"]=None):
        """Construction properties of the {@link CodeBuildAction CodeBuild build CodePipeline action}.

        :param action_name: The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param input: The source to use as input for this action.
        :param project: The action's Project.
        :param extra_inputs: The list of additional input Artifacts for this action.
        :param outputs: The list of output Artifacts for this action. **Note**: if you specify more than one output Artifact here, you cannot use the primary 'artifacts' section of the buildspec; you have to use the 'secondary-artifacts' section instead. See https://docs.aws.amazon.com/codebuild/latest/userguide/sample-multi-in-out.html for details. Default: the action will not have any outputs
        :param type: The type of the action that determines its CodePipeline Category - Build, or Test. Default: CodeBuildActionType.BUILD
        """
        self._values = {
            'action_name': action_name,
            'input': input,
            'project': project,
        }
        if run_order is not None: self._values["run_order"] = run_order
        if role is not None: self._values["role"] = role
        if extra_inputs is not None: self._values["extra_inputs"] = extra_inputs
        if outputs is not None: self._values["outputs"] = outputs
        if type is not None: self._values["type"] = type

    @property
    def action_name(self) -> str:
        """The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage."""
        return self._values.get('action_name')

    @property
    def run_order(self) -> typing.Optional[jsii.Number]:
        """The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        default
        :default: 1

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        """
        return self._values.get('run_order')

    @property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property.

        default
        :default: a new Role will be generated
        """
        return self._values.get('role')

    @property
    def input(self) -> aws_cdk.aws_codepipeline.Artifact:
        """The source to use as input for this action."""
        return self._values.get('input')

    @property
    def project(self) -> aws_cdk.aws_codebuild.IProject:
        """The action's Project."""
        return self._values.get('project')

    @property
    def extra_inputs(self) -> typing.Optional[typing.List[aws_cdk.aws_codepipeline.Artifact]]:
        """The list of additional input Artifacts for this action."""
        return self._values.get('extra_inputs')

    @property
    def outputs(self) -> typing.Optional[typing.List[aws_cdk.aws_codepipeline.Artifact]]:
        """The list of output Artifacts for this action. **Note**: if you specify more than one output Artifact here, you cannot use the primary 'artifacts' section of the buildspec; you have to use the 'secondary-artifacts' section instead. See https://docs.aws.amazon.com/codebuild/latest/userguide/sample-multi-in-out.html for details.

        default
        :default: the action will not have any outputs
        """
        return self._values.get('outputs')

    @property
    def type(self) -> typing.Optional["CodeBuildActionType"]:
        """The type of the action that determines its CodePipeline Category - Build, or Test.

        default
        :default: CodeBuildActionType.BUILD
        """
        return self._values.get('type')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CodeBuildActionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-codepipeline-actions.CodeBuildActionType")
class CodeBuildActionType(enum.Enum):
    """The type of the CodeBuild action that determines its CodePipeline Category - Build, or Test. The default is Build."""
    BUILD = "BUILD"
    """The action will have the Build Category. This is the default."""
    TEST = "TEST"
    """The action will have the Test Category."""

class CodeCommitSourceAction(Action, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline-actions.CodeCommitSourceAction"):
    """CodePipeline Source that is provided by an AWS CodeCommit repository."""
    def __init__(self, *, output: aws_cdk.aws_codepipeline.Artifact, repository: aws_cdk.aws_codecommit.IRepository, branch: typing.Optional[str]=None, trigger: typing.Optional["CodeCommitTrigger"]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None) -> None:
        """
        :param props: -
        :param output: 
        :param repository: The CodeCommit repository.
        :param branch: Default: 'master'
        :param trigger: How should CodePipeline detect source changes for this Action. Default: CodeCommitTrigger.EVENTS
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        """
        props = CodeCommitSourceActionProps(output=output, repository=repository, branch=branch, trigger=trigger, role=role, action_name=action_name, run_order=run_order)

        jsii.create(CodeCommitSourceAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(self, _scope: aws_cdk.core.Construct, stage: aws_cdk.aws_codepipeline.IStage, *, bucket: aws_cdk.aws_s3.IBucket, role: aws_cdk.aws_iam.IRole) -> aws_cdk.aws_codepipeline.ActionConfig:
        """The method called when an Action is attached to a Pipeline. This method is guaranteed to be called only once for each Action instance.

        :param _scope: -
        :param stage: -
        :param options: -
        :param bucket: 
        :param role: 
        """
        options = aws_cdk.aws_codepipeline.ActionBindOptions(bucket=bucket, role=role)

        return jsii.invoke(self, "bound", [_scope, stage, options])


@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-actions.CodeCommitSourceActionProps", jsii_struct_bases=[aws_cdk.aws_codepipeline.CommonAwsActionProps], name_mapping={'action_name': 'actionName', 'run_order': 'runOrder', 'role': 'role', 'output': 'output', 'repository': 'repository', 'branch': 'branch', 'trigger': 'trigger'})
class CodeCommitSourceActionProps(aws_cdk.aws_codepipeline.CommonAwsActionProps):
    def __init__(self, *, action_name: str, run_order: typing.Optional[jsii.Number]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, output: aws_cdk.aws_codepipeline.Artifact, repository: aws_cdk.aws_codecommit.IRepository, branch: typing.Optional[str]=None, trigger: typing.Optional["CodeCommitTrigger"]=None):
        """Construction properties of the {@link CodeCommitSourceAction CodeCommit source CodePipeline Action}.

        :param action_name: The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param output: 
        :param repository: The CodeCommit repository.
        :param branch: Default: 'master'
        :param trigger: How should CodePipeline detect source changes for this Action. Default: CodeCommitTrigger.EVENTS
        """
        self._values = {
            'action_name': action_name,
            'output': output,
            'repository': repository,
        }
        if run_order is not None: self._values["run_order"] = run_order
        if role is not None: self._values["role"] = role
        if branch is not None: self._values["branch"] = branch
        if trigger is not None: self._values["trigger"] = trigger

    @property
    def action_name(self) -> str:
        """The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage."""
        return self._values.get('action_name')

    @property
    def run_order(self) -> typing.Optional[jsii.Number]:
        """The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        default
        :default: 1

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        """
        return self._values.get('run_order')

    @property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property.

        default
        :default: a new Role will be generated
        """
        return self._values.get('role')

    @property
    def output(self) -> aws_cdk.aws_codepipeline.Artifact:
        return self._values.get('output')

    @property
    def repository(self) -> aws_cdk.aws_codecommit.IRepository:
        """The CodeCommit repository."""
        return self._values.get('repository')

    @property
    def branch(self) -> typing.Optional[str]:
        """
        default
        :default: 'master'
        """
        return self._values.get('branch')

    @property
    def trigger(self) -> typing.Optional["CodeCommitTrigger"]:
        """How should CodePipeline detect source changes for this Action.

        default
        :default: CodeCommitTrigger.EVENTS
        """
        return self._values.get('trigger')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CodeCommitSourceActionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-codepipeline-actions.CodeCommitTrigger")
class CodeCommitTrigger(enum.Enum):
    """How should the CodeCommit Action detect changes. This is the type of the {@link CodeCommitSourceAction.trigger} property."""
    NONE = "NONE"
    """The Action will never detect changes - the Pipeline it's part of will only begin a run when explicitly started."""
    POLL = "POLL"
    """CodePipeline will poll the repository to detect changes."""
    EVENTS = "EVENTS"
    """CodePipeline will use CloudWatch Events to be notified of changes. This is the default method of detecting changes."""

class CodeDeployServerDeployAction(Action, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline-actions.CodeDeployServerDeployAction"):
    def __init__(self, *, deployment_group: aws_cdk.aws_codedeploy.IServerDeploymentGroup, input: aws_cdk.aws_codepipeline.Artifact, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None) -> None:
        """
        :param props: -
        :param deployment_group: The CodeDeploy server Deployment Group to deploy to.
        :param input: The source to use as input for deployment.
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        """
        props = CodeDeployServerDeployActionProps(deployment_group=deployment_group, input=input, role=role, action_name=action_name, run_order=run_order)

        jsii.create(CodeDeployServerDeployAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(self, _scope: aws_cdk.core.Construct, _stage: aws_cdk.aws_codepipeline.IStage, *, bucket: aws_cdk.aws_s3.IBucket, role: aws_cdk.aws_iam.IRole) -> aws_cdk.aws_codepipeline.ActionConfig:
        """The method called when an Action is attached to a Pipeline. This method is guaranteed to be called only once for each Action instance.

        :param _scope: -
        :param _stage: -
        :param options: -
        :param bucket: 
        :param role: 
        """
        options = aws_cdk.aws_codepipeline.ActionBindOptions(bucket=bucket, role=role)

        return jsii.invoke(self, "bound", [_scope, _stage, options])


@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-actions.CodeDeployServerDeployActionProps", jsii_struct_bases=[aws_cdk.aws_codepipeline.CommonAwsActionProps], name_mapping={'action_name': 'actionName', 'run_order': 'runOrder', 'role': 'role', 'deployment_group': 'deploymentGroup', 'input': 'input'})
class CodeDeployServerDeployActionProps(aws_cdk.aws_codepipeline.CommonAwsActionProps):
    def __init__(self, *, action_name: str, run_order: typing.Optional[jsii.Number]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, deployment_group: aws_cdk.aws_codedeploy.IServerDeploymentGroup, input: aws_cdk.aws_codepipeline.Artifact):
        """Construction properties of the {@link CodeDeployServerDeployAction CodeDeploy server deploy CodePipeline Action}.

        :param action_name: The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param deployment_group: The CodeDeploy server Deployment Group to deploy to.
        :param input: The source to use as input for deployment.
        """
        self._values = {
            'action_name': action_name,
            'deployment_group': deployment_group,
            'input': input,
        }
        if run_order is not None: self._values["run_order"] = run_order
        if role is not None: self._values["role"] = role

    @property
    def action_name(self) -> str:
        """The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage."""
        return self._values.get('action_name')

    @property
    def run_order(self) -> typing.Optional[jsii.Number]:
        """The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        default
        :default: 1

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        """
        return self._values.get('run_order')

    @property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property.

        default
        :default: a new Role will be generated
        """
        return self._values.get('role')

    @property
    def deployment_group(self) -> aws_cdk.aws_codedeploy.IServerDeploymentGroup:
        """The CodeDeploy server Deployment Group to deploy to."""
        return self._values.get('deployment_group')

    @property
    def input(self) -> aws_cdk.aws_codepipeline.Artifact:
        """The source to use as input for deployment."""
        return self._values.get('input')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'CodeDeployServerDeployActionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class EcrSourceAction(Action, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline-actions.EcrSourceAction"):
    """The ECR Repository source CodePipeline Action.

    Will trigger the pipeline as soon as the target tag in the repository
    changes, but only if there is a CloudTrail Trail in the account that
    captures the ECR event.
    """
    def __init__(self, *, output: aws_cdk.aws_codepipeline.Artifact, repository: aws_cdk.aws_ecr.IRepository, image_tag: typing.Optional[str]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None) -> None:
        """
        :param props: -
        :param output: 
        :param repository: The repository that will be watched for changes.
        :param image_tag: The image tag that will be checked for changes. Default: 'latest'
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        """
        props = EcrSourceActionProps(output=output, repository=repository, image_tag=image_tag, role=role, action_name=action_name, run_order=run_order)

        jsii.create(EcrSourceAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(self, _scope: aws_cdk.core.Construct, stage: aws_cdk.aws_codepipeline.IStage, *, bucket: aws_cdk.aws_s3.IBucket, role: aws_cdk.aws_iam.IRole) -> aws_cdk.aws_codepipeline.ActionConfig:
        """The method called when an Action is attached to a Pipeline. This method is guaranteed to be called only once for each Action instance.

        :param _scope: -
        :param stage: -
        :param options: -
        :param bucket: 
        :param role: 
        """
        options = aws_cdk.aws_codepipeline.ActionBindOptions(bucket=bucket, role=role)

        return jsii.invoke(self, "bound", [_scope, stage, options])


@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-actions.EcrSourceActionProps", jsii_struct_bases=[aws_cdk.aws_codepipeline.CommonAwsActionProps], name_mapping={'action_name': 'actionName', 'run_order': 'runOrder', 'role': 'role', 'output': 'output', 'repository': 'repository', 'image_tag': 'imageTag'})
class EcrSourceActionProps(aws_cdk.aws_codepipeline.CommonAwsActionProps):
    def __init__(self, *, action_name: str, run_order: typing.Optional[jsii.Number]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, output: aws_cdk.aws_codepipeline.Artifact, repository: aws_cdk.aws_ecr.IRepository, image_tag: typing.Optional[str]=None):
        """Construction properties of {@link EcrSourceAction}.

        :param action_name: The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param output: 
        :param repository: The repository that will be watched for changes.
        :param image_tag: The image tag that will be checked for changes. Default: 'latest'
        """
        self._values = {
            'action_name': action_name,
            'output': output,
            'repository': repository,
        }
        if run_order is not None: self._values["run_order"] = run_order
        if role is not None: self._values["role"] = role
        if image_tag is not None: self._values["image_tag"] = image_tag

    @property
    def action_name(self) -> str:
        """The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage."""
        return self._values.get('action_name')

    @property
    def run_order(self) -> typing.Optional[jsii.Number]:
        """The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        default
        :default: 1

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        """
        return self._values.get('run_order')

    @property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property.

        default
        :default: a new Role will be generated
        """
        return self._values.get('role')

    @property
    def output(self) -> aws_cdk.aws_codepipeline.Artifact:
        return self._values.get('output')

    @property
    def repository(self) -> aws_cdk.aws_ecr.IRepository:
        """The repository that will be watched for changes."""
        return self._values.get('repository')

    @property
    def image_tag(self) -> typing.Optional[str]:
        """The image tag that will be checked for changes.

        default
        :default: 'latest'
        """
        return self._values.get('image_tag')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EcrSourceActionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class EcsDeployAction(Action, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline-actions.EcsDeployAction"):
    """CodePipeline Action to deploy an ECS Service."""
    def __init__(self, *, service: aws_cdk.aws_ecs.BaseService, image_file: typing.Optional[aws_cdk.aws_codepipeline.ArtifactPath]=None, input: typing.Optional[aws_cdk.aws_codepipeline.Artifact]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None) -> None:
        """
        :param props: -
        :param service: The ECS Service to deploy.
        :param image_file: The name of the JSON image definitions file to use for deployments. The JSON file is a list of objects, each with 2 keys: ``name`` is the name of the container in the Task Definition, and ``imageUri`` is the Docker image URI you want to update your service with. Use this property if you want to use a different name for this file than the default 'imagedefinitions.json'. If you use this property, you don't need to specify the ``input`` property. Default: - one of this property, or ``input``, is required
        :param input: The input artifact that contains the JSON image definitions file to use for deployments. The JSON file is a list of objects, each with 2 keys: ``name`` is the name of the container in the Task Definition, and ``imageUri`` is the Docker image URI you want to update your service with. If you use this property, it's assumed the file is called 'imagedefinitions.json'. If your build uses a different file, leave this property empty, and use the ``imageFile`` property instead. Default: - one of this property, or ``imageFile``, is required
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        """
        props = EcsDeployActionProps(service=service, image_file=image_file, input=input, role=role, action_name=action_name, run_order=run_order)

        jsii.create(EcsDeployAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(self, _scope: aws_cdk.core.Construct, _stage: aws_cdk.aws_codepipeline.IStage, *, bucket: aws_cdk.aws_s3.IBucket, role: aws_cdk.aws_iam.IRole) -> aws_cdk.aws_codepipeline.ActionConfig:
        """The method called when an Action is attached to a Pipeline. This method is guaranteed to be called only once for each Action instance.

        :param _scope: -
        :param _stage: -
        :param options: -
        :param bucket: 
        :param role: 
        """
        options = aws_cdk.aws_codepipeline.ActionBindOptions(bucket=bucket, role=role)

        return jsii.invoke(self, "bound", [_scope, _stage, options])


@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-actions.EcsDeployActionProps", jsii_struct_bases=[aws_cdk.aws_codepipeline.CommonAwsActionProps], name_mapping={'action_name': 'actionName', 'run_order': 'runOrder', 'role': 'role', 'service': 'service', 'image_file': 'imageFile', 'input': 'input'})
class EcsDeployActionProps(aws_cdk.aws_codepipeline.CommonAwsActionProps):
    def __init__(self, *, action_name: str, run_order: typing.Optional[jsii.Number]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, service: aws_cdk.aws_ecs.BaseService, image_file: typing.Optional[aws_cdk.aws_codepipeline.ArtifactPath]=None, input: typing.Optional[aws_cdk.aws_codepipeline.Artifact]=None):
        """Construction properties of {@link EcsDeployAction}.

        :param action_name: The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param service: The ECS Service to deploy.
        :param image_file: The name of the JSON image definitions file to use for deployments. The JSON file is a list of objects, each with 2 keys: ``name`` is the name of the container in the Task Definition, and ``imageUri`` is the Docker image URI you want to update your service with. Use this property if you want to use a different name for this file than the default 'imagedefinitions.json'. If you use this property, you don't need to specify the ``input`` property. Default: - one of this property, or ``input``, is required
        :param input: The input artifact that contains the JSON image definitions file to use for deployments. The JSON file is a list of objects, each with 2 keys: ``name`` is the name of the container in the Task Definition, and ``imageUri`` is the Docker image URI you want to update your service with. If you use this property, it's assumed the file is called 'imagedefinitions.json'. If your build uses a different file, leave this property empty, and use the ``imageFile`` property instead. Default: - one of this property, or ``imageFile``, is required
        """
        self._values = {
            'action_name': action_name,
            'service': service,
        }
        if run_order is not None: self._values["run_order"] = run_order
        if role is not None: self._values["role"] = role
        if image_file is not None: self._values["image_file"] = image_file
        if input is not None: self._values["input"] = input

    @property
    def action_name(self) -> str:
        """The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage."""
        return self._values.get('action_name')

    @property
    def run_order(self) -> typing.Optional[jsii.Number]:
        """The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        default
        :default: 1

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        """
        return self._values.get('run_order')

    @property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property.

        default
        :default: a new Role will be generated
        """
        return self._values.get('role')

    @property
    def service(self) -> aws_cdk.aws_ecs.BaseService:
        """The ECS Service to deploy."""
        return self._values.get('service')

    @property
    def image_file(self) -> typing.Optional[aws_cdk.aws_codepipeline.ArtifactPath]:
        """The name of the JSON image definitions file to use for deployments. The JSON file is a list of objects, each with 2 keys: ``name`` is the name of the container in the Task Definition, and ``imageUri`` is the Docker image URI you want to update your service with. Use this property if you want to use a different name for this file than the default 'imagedefinitions.json'. If you use this property, you don't need to specify the ``input`` property.

        default
        :default: - one of this property, or ``input``, is required

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/pipelines-create.html#pipelines-create-image-definitions
        """
        return self._values.get('image_file')

    @property
    def input(self) -> typing.Optional[aws_cdk.aws_codepipeline.Artifact]:
        """The input artifact that contains the JSON image definitions file to use for deployments. The JSON file is a list of objects, each with 2 keys: ``name`` is the name of the container in the Task Definition, and ``imageUri`` is the Docker image URI you want to update your service with. If you use this property, it's assumed the file is called 'imagedefinitions.json'. If your build uses a different file, leave this property empty, and use the ``imageFile`` property instead.

        default
        :default: - one of this property, or ``imageFile``, is required

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/pipelines-create.html#pipelines-create-image-definitions
        """
        return self._values.get('input')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'EcsDeployActionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class GitHubSourceAction(Action, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline-actions.GitHubSourceAction"):
    """Source that is provided by a GitHub repository."""
    def __init__(self, *, oauth_token: aws_cdk.core.SecretValue, output: aws_cdk.aws_codepipeline.Artifact, owner: str, repo: str, branch: typing.Optional[str]=None, trigger: typing.Optional["GitHubTrigger"]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None) -> None:
        """
        :param props: -
        :param oauth_token: A GitHub OAuth token to use for authentication. It is recommended to use a Secrets Manager ``Secret`` to obtain the token: const oauth = cdk.SecretValue.secretsManager('my-github-token'); new GitHubSource(this, 'GitHubAction', { oauthToken: oauth, ... });
        :param output: 
        :param owner: The GitHub account/user that owns the repo.
        :param repo: The name of the repo, without the username.
        :param branch: The branch to use. Default: "master"
        :param trigger: How AWS CodePipeline should be triggered. With the default value "WEBHOOK", a webhook is created in GitHub that triggers the action With "POLL", CodePipeline periodically checks the source for changes With "None", the action is not triggered through changes in the source Default: GitHubTrigger.WEBHOOK
        :param action_name: The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        """
        props = GitHubSourceActionProps(oauth_token=oauth_token, output=output, owner=owner, repo=repo, branch=branch, trigger=trigger, action_name=action_name, run_order=run_order)

        jsii.create(GitHubSourceAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(self, scope: aws_cdk.core.Construct, stage: aws_cdk.aws_codepipeline.IStage, *, bucket: aws_cdk.aws_s3.IBucket, role: aws_cdk.aws_iam.IRole) -> aws_cdk.aws_codepipeline.ActionConfig:
        """The method called when an Action is attached to a Pipeline. This method is guaranteed to be called only once for each Action instance.

        :param scope: -
        :param stage: -
        :param _options: -
        :param bucket: 
        :param role: 
        """
        _options = aws_cdk.aws_codepipeline.ActionBindOptions(bucket=bucket, role=role)

        return jsii.invoke(self, "bound", [scope, stage, _options])


@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-actions.GitHubSourceActionProps", jsii_struct_bases=[aws_cdk.aws_codepipeline.CommonActionProps], name_mapping={'action_name': 'actionName', 'run_order': 'runOrder', 'oauth_token': 'oauthToken', 'output': 'output', 'owner': 'owner', 'repo': 'repo', 'branch': 'branch', 'trigger': 'trigger'})
class GitHubSourceActionProps(aws_cdk.aws_codepipeline.CommonActionProps):
    def __init__(self, *, action_name: str, run_order: typing.Optional[jsii.Number]=None, oauth_token: aws_cdk.core.SecretValue, output: aws_cdk.aws_codepipeline.Artifact, owner: str, repo: str, branch: typing.Optional[str]=None, trigger: typing.Optional["GitHubTrigger"]=None):
        """Construction properties of the {@link GitHubSourceAction GitHub source action}.

        :param action_name: The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param oauth_token: A GitHub OAuth token to use for authentication. It is recommended to use a Secrets Manager ``Secret`` to obtain the token: const oauth = cdk.SecretValue.secretsManager('my-github-token'); new GitHubSource(this, 'GitHubAction', { oauthToken: oauth, ... });
        :param output: 
        :param owner: The GitHub account/user that owns the repo.
        :param repo: The name of the repo, without the username.
        :param branch: The branch to use. Default: "master"
        :param trigger: How AWS CodePipeline should be triggered. With the default value "WEBHOOK", a webhook is created in GitHub that triggers the action With "POLL", CodePipeline periodically checks the source for changes With "None", the action is not triggered through changes in the source Default: GitHubTrigger.WEBHOOK
        """
        self._values = {
            'action_name': action_name,
            'oauth_token': oauth_token,
            'output': output,
            'owner': owner,
            'repo': repo,
        }
        if run_order is not None: self._values["run_order"] = run_order
        if branch is not None: self._values["branch"] = branch
        if trigger is not None: self._values["trigger"] = trigger

    @property
    def action_name(self) -> str:
        """The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage."""
        return self._values.get('action_name')

    @property
    def run_order(self) -> typing.Optional[jsii.Number]:
        """The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        default
        :default: 1

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        """
        return self._values.get('run_order')

    @property
    def oauth_token(self) -> aws_cdk.core.SecretValue:
        """A GitHub OAuth token to use for authentication.

        It is recommended to use a Secrets Manager ``Secret`` to obtain the token:

        const oauth = cdk.SecretValue.secretsManager('my-github-token');
        new GitHubSource(this, 'GitHubAction', { oauthToken: oauth, ... });
        """
        return self._values.get('oauth_token')

    @property
    def output(self) -> aws_cdk.aws_codepipeline.Artifact:
        return self._values.get('output')

    @property
    def owner(self) -> str:
        """The GitHub account/user that owns the repo."""
        return self._values.get('owner')

    @property
    def repo(self) -> str:
        """The name of the repo, without the username."""
        return self._values.get('repo')

    @property
    def branch(self) -> typing.Optional[str]:
        """The branch to use.

        default
        :default: "master"
        """
        return self._values.get('branch')

    @property
    def trigger(self) -> typing.Optional["GitHubTrigger"]:
        """How AWS CodePipeline should be triggered.

        With the default value "WEBHOOK", a webhook is created in GitHub that triggers the action
        With "POLL", CodePipeline periodically checks the source for changes
        With "None", the action is not triggered through changes in the source

        default
        :default: GitHubTrigger.WEBHOOK
        """
        return self._values.get('trigger')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'GitHubSourceActionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-codepipeline-actions.GitHubTrigger")
class GitHubTrigger(enum.Enum):
    """If and how the GitHub source action should be triggered."""
    NONE = "NONE"
    POLL = "POLL"
    WEBHOOK = "WEBHOOK"

@jsii.interface(jsii_type="@aws-cdk/aws-codepipeline-actions.IJenkinsProvider")
class IJenkinsProvider(aws_cdk.core.IConstruct, jsii.compat.Protocol):
    """A Jenkins provider.

    If you want to create a new Jenkins provider managed alongside your CDK code,
    instantiate the {@link JenkinsProvider} class directly.

    If you want to reference an already registered provider,
    use the {@link JenkinsProvider#fromJenkinsProviderAttributes} method.
    """
    @staticmethod
    def __jsii_proxy_class__():
        return _IJenkinsProviderProxy

    @property
    @jsii.member(jsii_name="providerName")
    def provider_name(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="serverUrl")
    def server_url(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="version")
    def version(self) -> str:
        ...


class _IJenkinsProviderProxy(jsii.proxy_for(aws_cdk.core.IConstruct)):
    """A Jenkins provider.

    If you want to create a new Jenkins provider managed alongside your CDK code,
    instantiate the {@link JenkinsProvider} class directly.

    If you want to reference an already registered provider,
    use the {@link JenkinsProvider#fromJenkinsProviderAttributes} method.
    """
    __jsii_type__ = "@aws-cdk/aws-codepipeline-actions.IJenkinsProvider"
    @property
    @jsii.member(jsii_name="providerName")
    def provider_name(self) -> str:
        return jsii.get(self, "providerName")

    @property
    @jsii.member(jsii_name="serverUrl")
    def server_url(self) -> str:
        return jsii.get(self, "serverUrl")

    @property
    @jsii.member(jsii_name="version")
    def version(self) -> str:
        return jsii.get(self, "version")


@jsii.implements(IJenkinsProvider)
class BaseJenkinsProvider(aws_cdk.core.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-codepipeline-actions.BaseJenkinsProvider"):
    @staticmethod
    def __jsii_proxy_class__():
        return _BaseJenkinsProviderProxy

    def __init__(self, scope: aws_cdk.core.Construct, id: str, version: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param version: -
        """
        jsii.create(BaseJenkinsProvider, self, [scope, id, version])

    @property
    @jsii.member(jsii_name="providerName")
    @abc.abstractmethod
    def provider_name(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="serverUrl")
    @abc.abstractmethod
    def server_url(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="version")
    def version(self) -> str:
        return jsii.get(self, "version")


class _BaseJenkinsProviderProxy(BaseJenkinsProvider):
    @property
    @jsii.member(jsii_name="providerName")
    def provider_name(self) -> str:
        return jsii.get(self, "providerName")

    @property
    @jsii.member(jsii_name="serverUrl")
    def server_url(self) -> str:
        return jsii.get(self, "serverUrl")


class JenkinsAction(Action, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline-actions.JenkinsAction"):
    """Jenkins build CodePipeline Action.

    see
    :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/tutorials-four-stage-pipeline.html
    """
    def __init__(self, *, jenkins_provider: "IJenkinsProvider", project_name: str, type: "JenkinsActionType", inputs: typing.Optional[typing.List[aws_cdk.aws_codepipeline.Artifact]]=None, outputs: typing.Optional[typing.List[aws_cdk.aws_codepipeline.Artifact]]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None) -> None:
        """
        :param props: -
        :param jenkins_provider: The Jenkins Provider for this Action.
        :param project_name: The name of the project (sometimes also called job, or task) on your Jenkins installation that will be invoked by this Action.
        :param type: The type of the Action - Build, or Test.
        :param inputs: The source to use as input for this build.
        :param outputs: 
        :param action_name: The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        """
        props = JenkinsActionProps(jenkins_provider=jenkins_provider, project_name=project_name, type=type, inputs=inputs, outputs=outputs, action_name=action_name, run_order=run_order)

        jsii.create(JenkinsAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(self, _scope: aws_cdk.core.Construct, _stage: aws_cdk.aws_codepipeline.IStage, *, bucket: aws_cdk.aws_s3.IBucket, role: aws_cdk.aws_iam.IRole) -> aws_cdk.aws_codepipeline.ActionConfig:
        """The method called when an Action is attached to a Pipeline. This method is guaranteed to be called only once for each Action instance.

        :param _scope: -
        :param _stage: -
        :param _options: -
        :param bucket: 
        :param role: 
        """
        _options = aws_cdk.aws_codepipeline.ActionBindOptions(bucket=bucket, role=role)

        return jsii.invoke(self, "bound", [_scope, _stage, _options])


@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-actions.JenkinsActionProps", jsii_struct_bases=[aws_cdk.aws_codepipeline.CommonActionProps], name_mapping={'action_name': 'actionName', 'run_order': 'runOrder', 'jenkins_provider': 'jenkinsProvider', 'project_name': 'projectName', 'type': 'type', 'inputs': 'inputs', 'outputs': 'outputs'})
class JenkinsActionProps(aws_cdk.aws_codepipeline.CommonActionProps):
    def __init__(self, *, action_name: str, run_order: typing.Optional[jsii.Number]=None, jenkins_provider: "IJenkinsProvider", project_name: str, type: "JenkinsActionType", inputs: typing.Optional[typing.List[aws_cdk.aws_codepipeline.Artifact]]=None, outputs: typing.Optional[typing.List[aws_cdk.aws_codepipeline.Artifact]]=None):
        """Construction properties of {@link JenkinsAction}.

        :param action_name: The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param jenkins_provider: The Jenkins Provider for this Action.
        :param project_name: The name of the project (sometimes also called job, or task) on your Jenkins installation that will be invoked by this Action.
        :param type: The type of the Action - Build, or Test.
        :param inputs: The source to use as input for this build.
        :param outputs: 
        """
        self._values = {
            'action_name': action_name,
            'jenkins_provider': jenkins_provider,
            'project_name': project_name,
            'type': type,
        }
        if run_order is not None: self._values["run_order"] = run_order
        if inputs is not None: self._values["inputs"] = inputs
        if outputs is not None: self._values["outputs"] = outputs

    @property
    def action_name(self) -> str:
        """The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage."""
        return self._values.get('action_name')

    @property
    def run_order(self) -> typing.Optional[jsii.Number]:
        """The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        default
        :default: 1

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        """
        return self._values.get('run_order')

    @property
    def jenkins_provider(self) -> "IJenkinsProvider":
        """The Jenkins Provider for this Action."""
        return self._values.get('jenkins_provider')

    @property
    def project_name(self) -> str:
        """The name of the project (sometimes also called job, or task) on your Jenkins installation that will be invoked by this Action.

        Example::
            # Example may have issues. See https://github.com/aws/jsii/issues/826
            "MyJob"
        """
        return self._values.get('project_name')

    @property
    def type(self) -> "JenkinsActionType":
        """The type of the Action - Build, or Test."""
        return self._values.get('type')

    @property
    def inputs(self) -> typing.Optional[typing.List[aws_cdk.aws_codepipeline.Artifact]]:
        """The source to use as input for this build."""
        return self._values.get('inputs')

    @property
    def outputs(self) -> typing.Optional[typing.List[aws_cdk.aws_codepipeline.Artifact]]:
        return self._values.get('outputs')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'JenkinsActionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-codepipeline-actions.JenkinsActionType")
class JenkinsActionType(enum.Enum):
    """The type of the Jenkins Action that determines its CodePipeline Category - Build, or Test. Note that a Jenkins provider, even if it has the same name, must be separately registered for each type."""
    BUILD = "BUILD"
    """The Action will have the Build Category."""
    TEST = "TEST"
    """The Action will have the Test Category."""

class JenkinsProvider(BaseJenkinsProvider, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline-actions.JenkinsProvider"):
    """A class representing Jenkins providers.

    see
    :see: #import
    """
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, provider_name: str, server_url: str, for_build: typing.Optional[bool]=None, for_test: typing.Optional[bool]=None, version: typing.Optional[str]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param provider_name: The name of the Jenkins provider that you set in the AWS CodePipeline plugin configuration of your Jenkins project.
        :param server_url: The base URL of your Jenkins server.
        :param for_build: Whether to immediately register a Jenkins Provider for the build category. The Provider will always be registered if you create a {@link JenkinsAction}. Default: false
        :param for_test: Whether to immediately register a Jenkins Provider for the test category. The Provider will always be registered if you create a {@link JenkinsTestAction}. Default: false
        :param version: The version of your provider. Default: '1'
        """
        props = JenkinsProviderProps(provider_name=provider_name, server_url=server_url, for_build=for_build, for_test=for_test, version=version)

        jsii.create(JenkinsProvider, self, [scope, id, props])

    @jsii.member(jsii_name="fromJenkinsProviderAttributes")
    @classmethod
    def from_jenkins_provider_attributes(cls, scope: aws_cdk.core.Construct, id: str, *, provider_name: str, server_url: str, version: typing.Optional[str]=None) -> "IJenkinsProvider":
        """Import a Jenkins provider registered either outside the CDK, or in a different CDK Stack.

        :param scope: the parent Construct for the new provider.
        :param id: the identifier of the new provider Construct.
        :param attrs: the properties used to identify the existing provider.
        :param provider_name: The name of the Jenkins provider that you set in the AWS CodePipeline plugin configuration of your Jenkins project.
        :param server_url: The base URL of your Jenkins server.
        :param version: The version of your provider. Default: '1'

        return
        :return: a new Construct representing a reference to an existing Jenkins provider
        """
        attrs = JenkinsProviderAttributes(provider_name=provider_name, server_url=server_url, version=version)

        return jsii.sinvoke(cls, "fromJenkinsProviderAttributes", [scope, id, attrs])

    @property
    @jsii.member(jsii_name="providerName")
    def provider_name(self) -> str:
        return jsii.get(self, "providerName")

    @property
    @jsii.member(jsii_name="serverUrl")
    def server_url(self) -> str:
        return jsii.get(self, "serverUrl")


@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-actions.JenkinsProviderAttributes", jsii_struct_bases=[], name_mapping={'provider_name': 'providerName', 'server_url': 'serverUrl', 'version': 'version'})
class JenkinsProviderAttributes():
    def __init__(self, *, provider_name: str, server_url: str, version: typing.Optional[str]=None):
        """Properties for importing an existing Jenkins provider.

        :param provider_name: The name of the Jenkins provider that you set in the AWS CodePipeline plugin configuration of your Jenkins project.
        :param server_url: The base URL of your Jenkins server.
        :param version: The version of your provider. Default: '1'
        """
        self._values = {
            'provider_name': provider_name,
            'server_url': server_url,
        }
        if version is not None: self._values["version"] = version

    @property
    def provider_name(self) -> str:
        """The name of the Jenkins provider that you set in the AWS CodePipeline plugin configuration of your Jenkins project.

        Example::
            # Example may have issues. See https://github.com/aws/jsii/issues/826
            "MyJenkinsProvider"
        """
        return self._values.get('provider_name')

    @property
    def server_url(self) -> str:
        """The base URL of your Jenkins server.

        Example::
            # Example may have issues. See https://github.com/aws/jsii/issues/826
            "http://myjenkins.com:8080"
        """
        return self._values.get('server_url')

    @property
    def version(self) -> typing.Optional[str]:
        """The version of your provider.

        default
        :default: '1'
        """
        return self._values.get('version')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'JenkinsProviderAttributes(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-actions.JenkinsProviderProps", jsii_struct_bases=[], name_mapping={'provider_name': 'providerName', 'server_url': 'serverUrl', 'for_build': 'forBuild', 'for_test': 'forTest', 'version': 'version'})
class JenkinsProviderProps():
    def __init__(self, *, provider_name: str, server_url: str, for_build: typing.Optional[bool]=None, for_test: typing.Optional[bool]=None, version: typing.Optional[str]=None):
        """
        :param provider_name: The name of the Jenkins provider that you set in the AWS CodePipeline plugin configuration of your Jenkins project.
        :param server_url: The base URL of your Jenkins server.
        :param for_build: Whether to immediately register a Jenkins Provider for the build category. The Provider will always be registered if you create a {@link JenkinsAction}. Default: false
        :param for_test: Whether to immediately register a Jenkins Provider for the test category. The Provider will always be registered if you create a {@link JenkinsTestAction}. Default: false
        :param version: The version of your provider. Default: '1'
        """
        self._values = {
            'provider_name': provider_name,
            'server_url': server_url,
        }
        if for_build is not None: self._values["for_build"] = for_build
        if for_test is not None: self._values["for_test"] = for_test
        if version is not None: self._values["version"] = version

    @property
    def provider_name(self) -> str:
        """The name of the Jenkins provider that you set in the AWS CodePipeline plugin configuration of your Jenkins project.

        Example::
            # Example may have issues. See https://github.com/aws/jsii/issues/826
            "MyJenkinsProvider"
        """
        return self._values.get('provider_name')

    @property
    def server_url(self) -> str:
        """The base URL of your Jenkins server.

        Example::
            # Example may have issues. See https://github.com/aws/jsii/issues/826
            "http://myjenkins.com:8080"
        """
        return self._values.get('server_url')

    @property
    def for_build(self) -> typing.Optional[bool]:
        """Whether to immediately register a Jenkins Provider for the build category. The Provider will always be registered if you create a {@link JenkinsAction}.

        default
        :default: false
        """
        return self._values.get('for_build')

    @property
    def for_test(self) -> typing.Optional[bool]:
        """Whether to immediately register a Jenkins Provider for the test category. The Provider will always be registered if you create a {@link JenkinsTestAction}.

        default
        :default: false
        """
        return self._values.get('for_test')

    @property
    def version(self) -> typing.Optional[str]:
        """The version of your provider.

        default
        :default: '1'
        """
        return self._values.get('version')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'JenkinsProviderProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class LambdaInvokeAction(Action, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline-actions.LambdaInvokeAction"):
    """CodePipeline invoke Action that is provided by an AWS Lambda function.

    see
    :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/actions-invoke-lambda-function.html
    """
    def __init__(self, *, lambda_: aws_cdk.aws_lambda.IFunction, inputs: typing.Optional[typing.List[aws_cdk.aws_codepipeline.Artifact]]=None, outputs: typing.Optional[typing.List[aws_cdk.aws_codepipeline.Artifact]]=None, user_parameters: typing.Optional[typing.Mapping[str,typing.Any]]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None) -> None:
        """
        :param props: -
        :param lambda_: The lambda function to invoke.
        :param inputs: The optional input Artifacts of the Action. A Lambda Action can have up to 5 inputs. The inputs will appear in the event passed to the Lambda, under the ``'CodePipeline.job'.data.inputArtifacts`` path. Default: the Action will not have any inputs
        :param outputs: The optional names of the output Artifacts of the Action. A Lambda Action can have up to 5 outputs. The outputs will appear in the event passed to the Lambda, under the ``'CodePipeline.job'.data.outputArtifacts`` path. It is the responsibility of the Lambda to upload ZIP files with the Artifact contents to the provided locations. Default: the Action will not have any outputs
        :param user_parameters: A set of key-value pairs that will be accessible to the invoked Lambda inside the event that the Pipeline will call it with.
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        """
        props = LambdaInvokeActionProps(lambda_=lambda_, inputs=inputs, outputs=outputs, user_parameters=user_parameters, role=role, action_name=action_name, run_order=run_order)

        jsii.create(LambdaInvokeAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(self, scope: aws_cdk.core.Construct, _stage: aws_cdk.aws_codepipeline.IStage, *, bucket: aws_cdk.aws_s3.IBucket, role: aws_cdk.aws_iam.IRole) -> aws_cdk.aws_codepipeline.ActionConfig:
        """The method called when an Action is attached to a Pipeline. This method is guaranteed to be called only once for each Action instance.

        :param scope: -
        :param _stage: -
        :param options: -
        :param bucket: 
        :param role: 
        """
        options = aws_cdk.aws_codepipeline.ActionBindOptions(bucket=bucket, role=role)

        return jsii.invoke(self, "bound", [scope, _stage, options])


@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-actions.LambdaInvokeActionProps", jsii_struct_bases=[aws_cdk.aws_codepipeline.CommonAwsActionProps], name_mapping={'action_name': 'actionName', 'run_order': 'runOrder', 'role': 'role', 'lambda_': 'lambda', 'inputs': 'inputs', 'outputs': 'outputs', 'user_parameters': 'userParameters'})
class LambdaInvokeActionProps(aws_cdk.aws_codepipeline.CommonAwsActionProps):
    def __init__(self, *, action_name: str, run_order: typing.Optional[jsii.Number]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, lambda_: aws_cdk.aws_lambda.IFunction, inputs: typing.Optional[typing.List[aws_cdk.aws_codepipeline.Artifact]]=None, outputs: typing.Optional[typing.List[aws_cdk.aws_codepipeline.Artifact]]=None, user_parameters: typing.Optional[typing.Mapping[str,typing.Any]]=None):
        """Construction properties of the {@link LambdaInvokeAction Lambda invoke CodePipeline Action}.

        :param action_name: The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param lambda_: The lambda function to invoke.
        :param inputs: The optional input Artifacts of the Action. A Lambda Action can have up to 5 inputs. The inputs will appear in the event passed to the Lambda, under the ``'CodePipeline.job'.data.inputArtifacts`` path. Default: the Action will not have any inputs
        :param outputs: The optional names of the output Artifacts of the Action. A Lambda Action can have up to 5 outputs. The outputs will appear in the event passed to the Lambda, under the ``'CodePipeline.job'.data.outputArtifacts`` path. It is the responsibility of the Lambda to upload ZIP files with the Artifact contents to the provided locations. Default: the Action will not have any outputs
        :param user_parameters: A set of key-value pairs that will be accessible to the invoked Lambda inside the event that the Pipeline will call it with.
        """
        self._values = {
            'action_name': action_name,
            'lambda_': lambda_,
        }
        if run_order is not None: self._values["run_order"] = run_order
        if role is not None: self._values["role"] = role
        if inputs is not None: self._values["inputs"] = inputs
        if outputs is not None: self._values["outputs"] = outputs
        if user_parameters is not None: self._values["user_parameters"] = user_parameters

    @property
    def action_name(self) -> str:
        """The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage."""
        return self._values.get('action_name')

    @property
    def run_order(self) -> typing.Optional[jsii.Number]:
        """The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        default
        :default: 1

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        """
        return self._values.get('run_order')

    @property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property.

        default
        :default: a new Role will be generated
        """
        return self._values.get('role')

    @property
    def lambda_(self) -> aws_cdk.aws_lambda.IFunction:
        """The lambda function to invoke."""
        return self._values.get('lambda_')

    @property
    def inputs(self) -> typing.Optional[typing.List[aws_cdk.aws_codepipeline.Artifact]]:
        """The optional input Artifacts of the Action. A Lambda Action can have up to 5 inputs. The inputs will appear in the event passed to the Lambda, under the ``'CodePipeline.job'.data.inputArtifacts`` path.

        default
        :default: the Action will not have any inputs

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/actions-invoke-lambda-function.html#actions-invoke-lambda-function-json-event-example
        """
        return self._values.get('inputs')

    @property
    def outputs(self) -> typing.Optional[typing.List[aws_cdk.aws_codepipeline.Artifact]]:
        """The optional names of the output Artifacts of the Action. A Lambda Action can have up to 5 outputs. The outputs will appear in the event passed to the Lambda, under the ``'CodePipeline.job'.data.outputArtifacts`` path. It is the responsibility of the Lambda to upload ZIP files with the Artifact contents to the provided locations.

        default
        :default: the Action will not have any outputs
        """
        return self._values.get('outputs')

    @property
    def user_parameters(self) -> typing.Optional[typing.Mapping[str,typing.Any]]:
        """A set of key-value pairs that will be accessible to the invoked Lambda inside the event that the Pipeline will call it with.

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/actions-invoke-lambda-function.html#actions-invoke-lambda-function-json-event-example
        """
        return self._values.get('user_parameters')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'LambdaInvokeActionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class ManualApprovalAction(Action, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline-actions.ManualApprovalAction"):
    """Manual approval action."""
    def __init__(self, *, additional_information: typing.Optional[str]=None, notification_topic: typing.Optional[aws_cdk.aws_sns.ITopic]=None, notify_emails: typing.Optional[typing.List[str]]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None) -> None:
        """
        :param props: -
        :param additional_information: Any additional information that you want to include in the notification email message.
        :param notification_topic: Optional SNS topic to send notifications to when an approval is pending.
        :param notify_emails: A list of email addresses to subscribe to notifications when this Action is pending approval. If this has been provided, but not ``notificationTopic``, a new Topic will be created.
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        """
        props = ManualApprovalActionProps(additional_information=additional_information, notification_topic=notification_topic, notify_emails=notify_emails, role=role, action_name=action_name, run_order=run_order)

        jsii.create(ManualApprovalAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(self, scope: aws_cdk.core.Construct, _stage: aws_cdk.aws_codepipeline.IStage, *, bucket: aws_cdk.aws_s3.IBucket, role: aws_cdk.aws_iam.IRole) -> aws_cdk.aws_codepipeline.ActionConfig:
        """The method called when an Action is attached to a Pipeline. This method is guaranteed to be called only once for each Action instance.

        :param scope: -
        :param _stage: -
        :param options: -
        :param bucket: 
        :param role: 
        """
        options = aws_cdk.aws_codepipeline.ActionBindOptions(bucket=bucket, role=role)

        return jsii.invoke(self, "bound", [scope, _stage, options])

    @property
    @jsii.member(jsii_name="notificationTopic")
    def notification_topic(self) -> typing.Optional[aws_cdk.aws_sns.ITopic]:
        return jsii.get(self, "notificationTopic")


@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-actions.ManualApprovalActionProps", jsii_struct_bases=[aws_cdk.aws_codepipeline.CommonAwsActionProps], name_mapping={'action_name': 'actionName', 'run_order': 'runOrder', 'role': 'role', 'additional_information': 'additionalInformation', 'notification_topic': 'notificationTopic', 'notify_emails': 'notifyEmails'})
class ManualApprovalActionProps(aws_cdk.aws_codepipeline.CommonAwsActionProps):
    def __init__(self, *, action_name: str, run_order: typing.Optional[jsii.Number]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, additional_information: typing.Optional[str]=None, notification_topic: typing.Optional[aws_cdk.aws_sns.ITopic]=None, notify_emails: typing.Optional[typing.List[str]]=None):
        """Construction properties of the {@link ManualApprovalAction}.

        :param action_name: The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param additional_information: Any additional information that you want to include in the notification email message.
        :param notification_topic: Optional SNS topic to send notifications to when an approval is pending.
        :param notify_emails: A list of email addresses to subscribe to notifications when this Action is pending approval. If this has been provided, but not ``notificationTopic``, a new Topic will be created.
        """
        self._values = {
            'action_name': action_name,
        }
        if run_order is not None: self._values["run_order"] = run_order
        if role is not None: self._values["role"] = role
        if additional_information is not None: self._values["additional_information"] = additional_information
        if notification_topic is not None: self._values["notification_topic"] = notification_topic
        if notify_emails is not None: self._values["notify_emails"] = notify_emails

    @property
    def action_name(self) -> str:
        """The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage."""
        return self._values.get('action_name')

    @property
    def run_order(self) -> typing.Optional[jsii.Number]:
        """The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        default
        :default: 1

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        """
        return self._values.get('run_order')

    @property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property.

        default
        :default: a new Role will be generated
        """
        return self._values.get('role')

    @property
    def additional_information(self) -> typing.Optional[str]:
        """Any additional information that you want to include in the notification email message."""
        return self._values.get('additional_information')

    @property
    def notification_topic(self) -> typing.Optional[aws_cdk.aws_sns.ITopic]:
        """Optional SNS topic to send notifications to when an approval is pending."""
        return self._values.get('notification_topic')

    @property
    def notify_emails(self) -> typing.Optional[typing.List[str]]:
        """A list of email addresses to subscribe to notifications when this Action is pending approval. If this has been provided, but not ``notificationTopic``, a new Topic will be created."""
        return self._values.get('notify_emails')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ManualApprovalActionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class S3DeployAction(Action, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline-actions.S3DeployAction"):
    """Deploys the sourceArtifact to Amazon S3."""
    def __init__(self, *, bucket: aws_cdk.aws_s3.IBucket, input: aws_cdk.aws_codepipeline.Artifact, extract: typing.Optional[bool]=None, object_key: typing.Optional[str]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None) -> None:
        """
        :param props: -
        :param bucket: The Amazon S3 bucket that is the deploy target.
        :param input: The input Artifact to deploy to Amazon S3.
        :param extract: Should the deploy action extract the artifact before deploying to Amazon S3. Default: true
        :param object_key: The key of the target object. This is required if extract is false.
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        """
        props = S3DeployActionProps(bucket=bucket, input=input, extract=extract, object_key=object_key, role=role, action_name=action_name, run_order=run_order)

        jsii.create(S3DeployAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(self, _scope: aws_cdk.core.Construct, _stage: aws_cdk.aws_codepipeline.IStage, *, bucket: aws_cdk.aws_s3.IBucket, role: aws_cdk.aws_iam.IRole) -> aws_cdk.aws_codepipeline.ActionConfig:
        """The method called when an Action is attached to a Pipeline. This method is guaranteed to be called only once for each Action instance.

        :param _scope: -
        :param _stage: -
        :param options: -
        :param bucket: 
        :param role: 
        """
        options = aws_cdk.aws_codepipeline.ActionBindOptions(bucket=bucket, role=role)

        return jsii.invoke(self, "bound", [_scope, _stage, options])


@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-actions.S3DeployActionProps", jsii_struct_bases=[aws_cdk.aws_codepipeline.CommonAwsActionProps], name_mapping={'action_name': 'actionName', 'run_order': 'runOrder', 'role': 'role', 'bucket': 'bucket', 'input': 'input', 'extract': 'extract', 'object_key': 'objectKey'})
class S3DeployActionProps(aws_cdk.aws_codepipeline.CommonAwsActionProps):
    def __init__(self, *, action_name: str, run_order: typing.Optional[jsii.Number]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, bucket: aws_cdk.aws_s3.IBucket, input: aws_cdk.aws_codepipeline.Artifact, extract: typing.Optional[bool]=None, object_key: typing.Optional[str]=None):
        """Construction properties of the {@link S3DeployAction S3 deploy Action}.

        :param action_name: The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param bucket: The Amazon S3 bucket that is the deploy target.
        :param input: The input Artifact to deploy to Amazon S3.
        :param extract: Should the deploy action extract the artifact before deploying to Amazon S3. Default: true
        :param object_key: The key of the target object. This is required if extract is false.
        """
        self._values = {
            'action_name': action_name,
            'bucket': bucket,
            'input': input,
        }
        if run_order is not None: self._values["run_order"] = run_order
        if role is not None: self._values["role"] = role
        if extract is not None: self._values["extract"] = extract
        if object_key is not None: self._values["object_key"] = object_key

    @property
    def action_name(self) -> str:
        """The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage."""
        return self._values.get('action_name')

    @property
    def run_order(self) -> typing.Optional[jsii.Number]:
        """The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        default
        :default: 1

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        """
        return self._values.get('run_order')

    @property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property.

        default
        :default: a new Role will be generated
        """
        return self._values.get('role')

    @property
    def bucket(self) -> aws_cdk.aws_s3.IBucket:
        """The Amazon S3 bucket that is the deploy target."""
        return self._values.get('bucket')

    @property
    def input(self) -> aws_cdk.aws_codepipeline.Artifact:
        """The input Artifact to deploy to Amazon S3."""
        return self._values.get('input')

    @property
    def extract(self) -> typing.Optional[bool]:
        """Should the deploy action extract the artifact before deploying to Amazon S3.

        default
        :default: true
        """
        return self._values.get('extract')

    @property
    def object_key(self) -> typing.Optional[str]:
        """The key of the target object.

        This is required if extract is false.
        """
        return self._values.get('object_key')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'S3DeployActionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class S3SourceAction(Action, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codepipeline-actions.S3SourceAction"):
    """Source that is provided by a specific Amazon S3 object.

    Will trigger the pipeline as soon as the S3 object changes, but only if there is
    a CloudTrail Trail in the account that captures the S3 event.
    """
    def __init__(self, *, bucket: aws_cdk.aws_s3.IBucket, bucket_key: str, output: aws_cdk.aws_codepipeline.Artifact, trigger: typing.Optional["S3Trigger"]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, action_name: str, run_order: typing.Optional[jsii.Number]=None) -> None:
        """
        :param props: -
        :param bucket: The Amazon S3 bucket that stores the source code.
        :param bucket_key: The key within the S3 bucket that stores the source code.
        :param output: 
        :param trigger: How should CodePipeline detect source changes for this Action. Note that if this is S3Trigger.EVENTS, you need to make sure to include the source Bucket in a CloudTrail Trail, as otherwise the CloudWatch Events will not be emitted. Default: S3Trigger.POLL
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param action_name: The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        """
        props = S3SourceActionProps(bucket=bucket, bucket_key=bucket_key, output=output, trigger=trigger, role=role, action_name=action_name, run_order=run_order)

        jsii.create(S3SourceAction, self, [props])

    @jsii.member(jsii_name="bound")
    def _bound(self, _scope: aws_cdk.core.Construct, stage: aws_cdk.aws_codepipeline.IStage, *, bucket: aws_cdk.aws_s3.IBucket, role: aws_cdk.aws_iam.IRole) -> aws_cdk.aws_codepipeline.ActionConfig:
        """The method called when an Action is attached to a Pipeline. This method is guaranteed to be called only once for each Action instance.

        :param _scope: -
        :param stage: -
        :param options: -
        :param bucket: 
        :param role: 
        """
        options = aws_cdk.aws_codepipeline.ActionBindOptions(bucket=bucket, role=role)

        return jsii.invoke(self, "bound", [_scope, stage, options])


@jsii.data_type(jsii_type="@aws-cdk/aws-codepipeline-actions.S3SourceActionProps", jsii_struct_bases=[aws_cdk.aws_codepipeline.CommonAwsActionProps], name_mapping={'action_name': 'actionName', 'run_order': 'runOrder', 'role': 'role', 'bucket': 'bucket', 'bucket_key': 'bucketKey', 'output': 'output', 'trigger': 'trigger'})
class S3SourceActionProps(aws_cdk.aws_codepipeline.CommonAwsActionProps):
    def __init__(self, *, action_name: str, run_order: typing.Optional[jsii.Number]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, bucket: aws_cdk.aws_s3.IBucket, bucket_key: str, output: aws_cdk.aws_codepipeline.Artifact, trigger: typing.Optional["S3Trigger"]=None):
        """Construction properties of the {@link S3SourceAction S3 source Action}.

        :param action_name: The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage.
        :param run_order: The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute. Default: 1
        :param role: The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property. Default: a new Role will be generated
        :param bucket: The Amazon S3 bucket that stores the source code.
        :param bucket_key: The key within the S3 bucket that stores the source code.
        :param output: 
        :param trigger: How should CodePipeline detect source changes for this Action. Note that if this is S3Trigger.EVENTS, you need to make sure to include the source Bucket in a CloudTrail Trail, as otherwise the CloudWatch Events will not be emitted. Default: S3Trigger.POLL
        """
        self._values = {
            'action_name': action_name,
            'bucket': bucket,
            'bucket_key': bucket_key,
            'output': output,
        }
        if run_order is not None: self._values["run_order"] = run_order
        if role is not None: self._values["role"] = role
        if trigger is not None: self._values["trigger"] = trigger

    @property
    def action_name(self) -> str:
        """The physical, human-readable name of the Action. Not that Action names must be unique within a single Stage."""
        return self._values.get('action_name')

    @property
    def run_order(self) -> typing.Optional[jsii.Number]:
        """The runOrder property for this Action. RunOrder determines the relative order in which multiple Actions in the same Stage execute.

        default
        :default: 1

        see
        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html
        """
        return self._values.get('run_order')

    @property
    def role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The Role in which context's this Action will be executing in. The Pipeline's Role will assume this Role (the required permissions for that will be granted automatically) right before executing this Action. This Action will be passed into your {@link IAction.bind} method in the {@link ActionBindOptions.role} property.

        default
        :default: a new Role will be generated
        """
        return self._values.get('role')

    @property
    def bucket(self) -> aws_cdk.aws_s3.IBucket:
        """The Amazon S3 bucket that stores the source code."""
        return self._values.get('bucket')

    @property
    def bucket_key(self) -> str:
        """The key within the S3 bucket that stores the source code.

        Example::
            # Example may have issues. See https://github.com/aws/jsii/issues/826
            "path/to/file.zip"
        """
        return self._values.get('bucket_key')

    @property
    def output(self) -> aws_cdk.aws_codepipeline.Artifact:
        return self._values.get('output')

    @property
    def trigger(self) -> typing.Optional["S3Trigger"]:
        """How should CodePipeline detect source changes for this Action. Note that if this is S3Trigger.EVENTS, you need to make sure to include the source Bucket in a CloudTrail Trail, as otherwise the CloudWatch Events will not be emitted.

        default
        :default: S3Trigger.POLL

        see
        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/log-s3-data-events.html
        """
        return self._values.get('trigger')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'S3SourceActionProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.enum(jsii_type="@aws-cdk/aws-codepipeline-actions.S3Trigger")
class S3Trigger(enum.Enum):
    """How should the S3 Action detect changes. This is the type of the {@link S3SourceAction.trigger} property."""
    NONE = "NONE"
    """The Action will never detect changes - the Pipeline it's part of will only begin a run when explicitly started."""
    POLL = "POLL"
    """CodePipeline will poll S3 to detect changes. This is the default method of detecting changes."""
    EVENTS = "EVENTS"
    """CodePipeline will use CloudWatch Events to be notified of changes. Note that the Bucket that the Action uses needs to be part of a CloudTrail Trail for the events to be delivered."""

__all__ = ["Action", "AlexaSkillDeployAction", "AlexaSkillDeployActionProps", "BaseJenkinsProvider", "CloudFormationCreateReplaceChangeSetAction", "CloudFormationCreateReplaceChangeSetActionProps", "CloudFormationCreateUpdateStackAction", "CloudFormationCreateUpdateStackActionProps", "CloudFormationDeleteStackAction", "CloudFormationDeleteStackActionProps", "CloudFormationExecuteChangeSetAction", "CloudFormationExecuteChangeSetActionProps", "CodeBuildAction", "CodeBuildActionProps", "CodeBuildActionType", "CodeCommitSourceAction", "CodeCommitSourceActionProps", "CodeCommitTrigger", "CodeDeployServerDeployAction", "CodeDeployServerDeployActionProps", "EcrSourceAction", "EcrSourceActionProps", "EcsDeployAction", "EcsDeployActionProps", "GitHubSourceAction", "GitHubSourceActionProps", "GitHubTrigger", "IJenkinsProvider", "JenkinsAction", "JenkinsActionProps", "JenkinsActionType", "JenkinsProvider", "JenkinsProviderAttributes", "JenkinsProviderProps", "LambdaInvokeAction", "LambdaInvokeActionProps", "ManualApprovalAction", "ManualApprovalActionProps", "S3DeployAction", "S3DeployActionProps", "S3SourceAction", "S3SourceActionProps", "S3Trigger", "__jsii_assembly__"]

publication.publish()
