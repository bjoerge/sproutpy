import {defineConfig} from 'sanity'
import {deskTool} from 'sanity/desk'
import {visionTool} from '@sanity/vision'
import {schemaTypes} from './src/schemas'
import {readEnv} from './src/utils/readEnv'
import {Box} from '@sanity/ui'

export default defineConfig({
  name: 'default',
  title: '🪴 Sproutpy Studio',

  projectId: readEnv(process.env, 'SANITY_STUDIO_PROJECT_ID'),
  dataset: readEnv(process.env, 'SANITY_STUDIO_DATASET'),

  plugins: [deskTool(), visionTool()],

  schema: {
    types: schemaTypes,
  },
})
