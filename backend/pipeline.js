var source = mongodb({
  "uri": "${MONGODB_URI}"
})

var sink = elasticsearch({
  "uri": "${ELASTICSEARCH_URI}"
})
t.Source("source", source, "/.*/").Save("sink", sink, "/.*/")
