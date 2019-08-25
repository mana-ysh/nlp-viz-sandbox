/**
 * Define all of your application routes here
 * for more information on routes, see the
 * official documentation https://router.vuejs.org/en/
 */
export default [
  {
    path: '',
    // Relative to /src/views
    view: 'TopPage'
  },
  {
    path: '/text-analysis',
    name: 'Fundamental text analysis',
    view: 'TextAnalysis'
  },
  {
    path: '/language-model',
    name: 'Language model',
    view: 'LanguageModel'
  }
]
