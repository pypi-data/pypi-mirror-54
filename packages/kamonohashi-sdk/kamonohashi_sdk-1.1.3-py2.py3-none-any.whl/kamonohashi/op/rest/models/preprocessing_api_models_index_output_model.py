# coding: utf-8

"""
    KAMONOHASHI API

    A platform for deep learning  # noqa: E501

    OpenAPI spec version: v1
    Contact: kamonohashi-support@jp.nssol.nipponsteel.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class PreprocessingApiModelsIndexOutputModel(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'cpu': 'int',
        'created_at': 'str',
        'created_by': 'str',
        'gpu': 'int',
        'id': 'int',
        'memo': 'str',
        'memory': 'int',
        'modified_at': 'str',
        'modified_by': 'str',
        'name': 'str'
    }

    attribute_map = {
        'cpu': 'cpu',
        'created_at': 'createdAt',
        'created_by': 'createdBy',
        'gpu': 'gpu',
        'id': 'id',
        'memo': 'memo',
        'memory': 'memory',
        'modified_at': 'modifiedAt',
        'modified_by': 'modifiedBy',
        'name': 'name'
    }

    def __init__(self, cpu=None, created_at=None, created_by=None, gpu=None, id=None, memo=None, memory=None, modified_at=None, modified_by=None, name=None):  # noqa: E501
        """PreprocessingApiModelsIndexOutputModel - a model defined in Swagger"""  # noqa: E501

        self._cpu = None
        self._created_at = None
        self._created_by = None
        self._gpu = None
        self._id = None
        self._memo = None
        self._memory = None
        self._modified_at = None
        self._modified_by = None
        self._name = None
        self.discriminator = None

        if cpu is not None:
            self.cpu = cpu
        if created_at is not None:
            self.created_at = created_at
        if created_by is not None:
            self.created_by = created_by
        if gpu is not None:
            self.gpu = gpu
        if id is not None:
            self.id = id
        if memo is not None:
            self.memo = memo
        if memory is not None:
            self.memory = memory
        if modified_at is not None:
            self.modified_at = modified_at
        if modified_by is not None:
            self.modified_by = modified_by
        if name is not None:
            self.name = name

    @property
    def cpu(self):
        """Gets the cpu of this PreprocessingApiModelsIndexOutputModel.  # noqa: E501


        :return: The cpu of this PreprocessingApiModelsIndexOutputModel.  # noqa: E501
        :rtype: int
        """
        return self._cpu

    @cpu.setter
    def cpu(self, cpu):
        """Sets the cpu of this PreprocessingApiModelsIndexOutputModel.


        :param cpu: The cpu of this PreprocessingApiModelsIndexOutputModel.  # noqa: E501
        :type: int
        """

        self._cpu = cpu

    @property
    def created_at(self):
        """Gets the created_at of this PreprocessingApiModelsIndexOutputModel.  # noqa: E501


        :return: The created_at of this PreprocessingApiModelsIndexOutputModel.  # noqa: E501
        :rtype: str
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this PreprocessingApiModelsIndexOutputModel.


        :param created_at: The created_at of this PreprocessingApiModelsIndexOutputModel.  # noqa: E501
        :type: str
        """

        self._created_at = created_at

    @property
    def created_by(self):
        """Gets the created_by of this PreprocessingApiModelsIndexOutputModel.  # noqa: E501


        :return: The created_by of this PreprocessingApiModelsIndexOutputModel.  # noqa: E501
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """Sets the created_by of this PreprocessingApiModelsIndexOutputModel.


        :param created_by: The created_by of this PreprocessingApiModelsIndexOutputModel.  # noqa: E501
        :type: str
        """

        self._created_by = created_by

    @property
    def gpu(self):
        """Gets the gpu of this PreprocessingApiModelsIndexOutputModel.  # noqa: E501


        :return: The gpu of this PreprocessingApiModelsIndexOutputModel.  # noqa: E501
        :rtype: int
        """
        return self._gpu

    @gpu.setter
    def gpu(self, gpu):
        """Sets the gpu of this PreprocessingApiModelsIndexOutputModel.


        :param gpu: The gpu of this PreprocessingApiModelsIndexOutputModel.  # noqa: E501
        :type: int
        """

        self._gpu = gpu

    @property
    def id(self):
        """Gets the id of this PreprocessingApiModelsIndexOutputModel.  # noqa: E501


        :return: The id of this PreprocessingApiModelsIndexOutputModel.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this PreprocessingApiModelsIndexOutputModel.


        :param id: The id of this PreprocessingApiModelsIndexOutputModel.  # noqa: E501
        :type: int
        """

        self._id = id

    @property
    def memo(self):
        """Gets the memo of this PreprocessingApiModelsIndexOutputModel.  # noqa: E501


        :return: The memo of this PreprocessingApiModelsIndexOutputModel.  # noqa: E501
        :rtype: str
        """
        return self._memo

    @memo.setter
    def memo(self, memo):
        """Sets the memo of this PreprocessingApiModelsIndexOutputModel.


        :param memo: The memo of this PreprocessingApiModelsIndexOutputModel.  # noqa: E501
        :type: str
        """

        self._memo = memo

    @property
    def memory(self):
        """Gets the memory of this PreprocessingApiModelsIndexOutputModel.  # noqa: E501


        :return: The memory of this PreprocessingApiModelsIndexOutputModel.  # noqa: E501
        :rtype: int
        """
        return self._memory

    @memory.setter
    def memory(self, memory):
        """Sets the memory of this PreprocessingApiModelsIndexOutputModel.


        :param memory: The memory of this PreprocessingApiModelsIndexOutputModel.  # noqa: E501
        :type: int
        """

        self._memory = memory

    @property
    def modified_at(self):
        """Gets the modified_at of this PreprocessingApiModelsIndexOutputModel.  # noqa: E501


        :return: The modified_at of this PreprocessingApiModelsIndexOutputModel.  # noqa: E501
        :rtype: str
        """
        return self._modified_at

    @modified_at.setter
    def modified_at(self, modified_at):
        """Sets the modified_at of this PreprocessingApiModelsIndexOutputModel.


        :param modified_at: The modified_at of this PreprocessingApiModelsIndexOutputModel.  # noqa: E501
        :type: str
        """

        self._modified_at = modified_at

    @property
    def modified_by(self):
        """Gets the modified_by of this PreprocessingApiModelsIndexOutputModel.  # noqa: E501


        :return: The modified_by of this PreprocessingApiModelsIndexOutputModel.  # noqa: E501
        :rtype: str
        """
        return self._modified_by

    @modified_by.setter
    def modified_by(self, modified_by):
        """Sets the modified_by of this PreprocessingApiModelsIndexOutputModel.


        :param modified_by: The modified_by of this PreprocessingApiModelsIndexOutputModel.  # noqa: E501
        :type: str
        """

        self._modified_by = modified_by

    @property
    def name(self):
        """Gets the name of this PreprocessingApiModelsIndexOutputModel.  # noqa: E501


        :return: The name of this PreprocessingApiModelsIndexOutputModel.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this PreprocessingApiModelsIndexOutputModel.


        :param name: The name of this PreprocessingApiModelsIndexOutputModel.  # noqa: E501
        :type: str
        """

        self._name = name

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(PreprocessingApiModelsIndexOutputModel, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, PreprocessingApiModelsIndexOutputModel):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
