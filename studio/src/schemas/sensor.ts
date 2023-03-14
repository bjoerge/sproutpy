import {defineType} from 'sanity'
import formatDistanceToNow from 'date-fns/formatDistanceToNow'
import {ActivityIcon} from '@sanity/icons'

export const measurement = defineType({
  type: 'object',
  name: 'measurement',
  title: 'Sensor measurement',
  options: {columns: 2},
  fields: [
    {name: 'value', title: 'Sensor value', type: 'number'},
    {
      name: 'timestamp',
      type: 'datetime',
      title: 'Date',
      options: {
        timeFormat: 'HH:mm:ss',
      },
    },
  ],
  preview: {
    select: {value: 'value', timestamp: 'timestamp'},
    prepare: ({value, timestamp}) => {
      return {
        title: `${value ?? 'n/a'}`,
        subtitle: `${formatDistanceToNow(new Date(timestamp))} ago`,
      }
    },
  },
})

export const sensor = defineType({
  name: 'sensor',
  type: 'document',
  title: 'Sensor',
  liveEdit: true,
  icon: ActivityIcon,
  fields: [
    {
      name: 'title',
      title: 'Title',
      description: 'An optional, chosen name for this sensor, e.g. Monstera Livingroom Corner',
      type: 'string',
    },
    {
      name: 'type',
      title: 'Sensor type',
      description: 'Set by the device',
      readOnly: true,
      type: 'string',
    },
    {
      name: 'name',
      title: 'Device name',
      description: 'Set by the device',
      readOnly: true,
      type: 'string',
    },
    {
      name: 'latest',
      title: 'Latest sensor reading',
      description: 'Set by the device',
      readOnly: true,
      type: 'measurement',
    },
    {
      name: 'measurements',
      title: 'Recent measurements',
      description: 'Set by the device, capped at 200 items',
      type: 'array',
      // readOnly: true,
      of: [{type: 'measurement'}],
    },
  ],
  preview: {
    select: {
      title: 'title',
      name: 'name',
      type: 'type',
      latest: 'latest'
    },
    prepare(val: any) {

      return {
        title: val.title || val.name,
        subtitle: val.latest?.value
          ? `${val.latest.value}, ${formatDistanceToNow(new Date(val.latest.timestamp))} ago`
          : 'n/a',
      }
    },
  },

})
