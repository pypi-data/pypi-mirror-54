# Copyright 2018 Iguazio
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ..model import RunObject
from ..utils import update_in, logger, get_in
from .base import BaseRuntime, RunError
import nuclio


class NuclioDeployRuntime(BaseRuntime):
    kind = 'nuclio'
    def __init__(self, metadata=None, spec=None):
        super().__init__(metadata, spec)
        self._config = None
        self.dashboard = ''

    # TODO: dashboard from command
    # TODO: runtime should use nuclio deploy_file + kinds

    def _run(self, runobj: RunObject, execution):

        from nuclio.deploy import deploy_config

        extra_env = [{'name': 'MLRUN_EXEC_CONFIG', 'value': runobj.to_json()}]
        if self.spec.rundb:
            extra_env.append({'name': 'MLRUN_DBPATH', 'value': self.spec.rundb})

        update_in(runtime, 'spec.env', extra_env, append=True)

        uid = runobj.metadata.uid
        update_in(runtime, 'metadata.labels.mlrun/class', self.kind)
        update_in(runtime, 'metadata.labels.mlrun/uid', uid)
        if runobj.metadata.name:
            update_in(runtime, 'metadata.name', runobj.metadata.name)
            runtime.metadata.name = runobj.metadata.name
        name = get_in(runtime, 'metadata.name', '')
        project = runobj.metadata.project

        if not project or not name:
            raise RunError('name and a project must be specified in the run to deploy this function')

        addr = deploy_config(runtime, self.dashboard, name, project, create_new=True)
        logger.info('function address is {}'.format(addr))
        return None

