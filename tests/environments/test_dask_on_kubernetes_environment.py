import pytest

import prefect
from prefect.environments import k8s

#################################
##### DaskOnKubernetes Tests
#################################


class TestDaskOnKubernetesEnvironment:
    def test_create_dask_on_k8s_environment(self):
        env = k8s.DaskOnKubernetesEnvironment(base_image="a")
        assert env

    def test_dask_on_k8s_environment_has_default_image(self):
        env = k8s.DaskOnKubernetesEnvironment()
        assert env.base_image == "python:3.6"

    def test_dask_on_k8s_environment_variables(self):
        env = k8s.DaskOnKubernetesEnvironment(
            base_image="a",
            registry_url="b",
            python_dependencies=["c"],
            image_name="d",
            image_tag="e",
            env_vars={"f": "g"},
            files={"/": "/"},
            max_workers=5,
        )
        assert env.base_image == "a"
        assert env.registry_url == "b"
        assert env.python_dependencies == ["c"]
        assert env.image_name == "d"
        assert env.image_tag == "e"
        assert env.env_vars == {"f": "g"}
        assert env.files == {"/": "/"}
        assert env.max_workers == 5

    def test_dask_on_k8s_environment_default_workers(self):
        env = k8s.DaskOnKubernetesEnvironment(base_image="a")
        assert env.max_workers == 1

    def test_dask_on_k8s_environment_default_scheduler_address_is_none(self):
        env = k8s.DaskOnKubernetesEnvironment(base_image="a")
        assert env.scheduler_address == None

    def test_dask_on_k8s_environment_identifier_label(self):
        env = k8s.DaskOnKubernetesEnvironment(base_image="a")
        assert env.identifier_label

    def test_dask_on_k8s_environment_setup_does_nothing(self):
        env = k8s.DaskOnKubernetesEnvironment(base_image="a")
        env.setup()
        assert env

    @pytest.mark.xfail(raises=ImportError)
    def test_dask_on_k8s_environment_execution_raises_error_out_of_cluster(self):
        env = k8s.DaskOnKubernetesEnvironment(base_image="a")
        with pytest.raises(EnvironmentError) as exc:
            env.execute()
        assert "Environment not currently inside a cluster" in str(exc.value)
