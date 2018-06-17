#!/bin/bash

function fatal() {
  echo "error: $@";
  exit 1;
}

if [ $# -ne 1 ]; then
    echo "Usage: $0 [JSon file]";
    exit 1;
fi

case "$(uname -s)" in
   Darwin)
     sedopt="-E";
     ;;
   *)
     sedopt="-r";
     ;;
esac

regex="^{\([^:]*\):\[\[\([^]]*\)\],\[\([^]]*\)\],\[\(.*\)\],\[\([^]]*\)\],\[\([^]]*\)\]\]}$";

in="$1";
[ -f "${in}" ] || fatal "Invalid input file";

flat=$(cat "${in}" | tr -d " \r\n");

tmp=$(echo "${flat}" | sed "s/${regex}//");
[ -z "${tmp}" ] || fatal "Invalid json format";

content=$(echo "${flat}" | sed "s/${regex}/\1;\2;\3;\4;\5;\6/");

name=$(echo "${content}" | cut -f 1 -d";");
trans=($(echo "${content}" | cut -f 4 -d";" | sed ${sedopt} "s/(\[[^]]*\]),?/\1 /g"));
initials=($(echo "${content}" | cut -f 5 -d";" | sed ${sedopt} "s/(\"[^\"]*\"),?/\1 /g"));
finals=($(echo "${content}" | cut -f 6 -d";" | sed ${sedopt} "s/(\"[^\"]*\"),?/\1 /g"));

echo "digraph ${name} {";

x=0;
for i in "${initials[@]}"; do
    echo "    _nil${x} [style=\"invis\"]";
    echo "    _nil${x} -> ${i} [label=\"\"]";
    ((x++));
done

for t in "${trans[@]}"; do
  tmp=$(echo $t | sed "s/^\[\(\".*\"\),\(\".*\"\),\(\".*\"\)\]$/\1;\2;\3/");

  from=$(echo "${tmp}" | cut -f 1 -d";");
  symbol=$(echo "${tmp}" | cut -f 2 -d";");
  to=$(echo "${tmp}" | cut -f 3 -d";");

  echo "    ${from} -> ${to} [label=${symbol}]";
done

for f in "${finals[@]}"; do
  echo "    ${f} [peripheries=2]";
done

echo "}";
