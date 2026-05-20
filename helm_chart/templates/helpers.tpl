{{/*
Return the chart full name
*/}}
{{- define "netpol.fullname" -}}
{{- $name := printf "%s-%s" .Release.Name .Chart.Name -}}
{{- $name | replace "_" "-" | lower | trunc 63 | trimSuffix "-" -}}
{{- end -}}