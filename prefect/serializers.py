import abc
import ujson


class Serializer(metaclass=abc.ABCMeta):
    """
    Prefect tasks can produce results that are in turn consumed by other tasks.
    Serializers are used to efficiently transmit those results.

    Simple results can be passed directly between tasks, but larger or more
    complex objects may require special handling.

    Serializers implement two key methods: encode() and decode(). Note:

    Encode() is passed the result of a task and a key that uniquely identifies
    that result. It must return a JSON-serializeable object that can be used
    to retrieve the serialized result.

    The result of encode() is passed to decode() when the task result is
    required. Decode() is expected to return the original task result.

    Serializers may be instantiated seperately for encoding and decoding,
    so methods should not depend on shared state.
    """

    @abc.abstractmethod
    def encode(key, result):
        """
        Serialize a task run result.

        This method is passed a unique key and a result. It is expected to
        serialize the result and return a JSON-serializeable object that
        can be used to reconstruct the original result.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def decode(encoded_result):
        raise NotImplementedError()


class JSONSerializer(Serializer):
    """
    Serializes task results to JSON
    """

    def encode(key, result):
        return ujson.dumps(result)

    def decode(encoded_result):
        return ujson.loads(encoded_result)