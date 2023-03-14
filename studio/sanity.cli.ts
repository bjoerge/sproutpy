import {defineCliConfig} from 'sanity/cli'
import {readEnv} from './src/utils/readEnv'

export default defineCliConfig({
  api: {
    projectId: readEnv(process.env, 'SANITY_STUDIO_PROJECT_ID'),
    dataset: readEnv(process.env, 'SANITY_STUDIO_DATASET'),
  },
})
