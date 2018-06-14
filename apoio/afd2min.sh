#!/bin/bash

function fatal() {
  echo "error: $@";
  exit 1;
}

function set_transition() {
  local name="${1}";
  local from="${2}";
  local symbol="${3}";
  local to="${4}";

  eval ${name}__${from}__${symbol}=${to};
}

function get_transition() {
  local name="$1";
  local from="$2";
  local symbol="$3";

  eval echo \${${name}__${from}__${symbol}};
}

function complete_afd() {
  local name="$1";
  local error="";
  local s;
  local a;
  local a2;

  for s in $(eval echo \${${name}_states[@]}); do
    for a in $(eval echo \${${name}_alphabet[@]}); do
      local to=$(get_transition "${name}" "${s}" "${a}");
      if [ -z "${to}" ]; then
        if [ -z "$error" ]; then
          error="error";
          for a2 in $(eval echo \${${name}_alphabet[@]}); do
            set_transition "${name}" "${error}" "${a2}" "${error}";
          done

          eval ${name}_states[\${#${name}_states[@]}]="${error}";
        fi

        set_transition "${name}" "${s}" "${a}" "${error}";
      fi
    done
  done
}

function clear_afd() {
  local name="$1";
  local s;
  local a;

  for s in $(eval echo \${${name}_states[@]}); do
    for a in $(eval echo \${${name}_alphabet[@]}); do
      eval "unset ${name}__${s}__${a}";
    done
  done

  unset "${name}_states";
  unset "${name}_alphabet";
  unset "${name}_trans";
  unset "${name}_initials";
  unset "${name}_finals";
}

function print_afd() {
  local name="$1";
  local s;
  local a;

  for s in "$(eval echo \${${name}_states[@]})"; do
    for a in "$(eval echo \${${name}_alphabet[@]})"; do
      local to=$(get_transition "${name}" "${s}" "${a}");
      echo "[$s, $a] = ${to}";
    done
  done
}

function to_dot() {
  local name="$1";

  echo "digraph \"af\" {";

  local x=0;
  local i;
  for i in $(eval echo \${${name}_initials[@]}); do
    echo "    _nil${x} [style=\"invis\"]";
    echo "    _nil${x} -> \"${i}\" [label=\"\"]";
    ((x++));
  done

  local s;
  local a;
  for s in $(eval echo \${${name}_states[@]}); do
    for a in $(eval echo \${${name}_alphabet[@]}); do
      local to=$(get_transition "${name}" "${s}" "${a}");
      if [ -n "${to}" ]; then
        echo "    \"${s}\" -> \"${to}\" [label=\"${a}\"]";
      fi
    done
  done

  local f;
  for f in $(eval echo \${${name}_finals[@]}); do
    echo "    \"${f}\" [peripheries=2]";
  done

  echo "}";
}

function contains_in() {
  local value=$1;
  local v;

  shift;
  for v; do
    [ "$v" == "$value" ] && return 0;
  done

  return 1;
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

#name=$(echo "${content}" | cut -f 1 -d";");
original_states=($(echo "${content}" | cut -f 2 -d";" | sed ${sedopt} "s/\"([^\"]*)\",?/\1 /g" | tr "," "_" ));
original_alphabet=($(echo "${content}" | cut -f 3 -d";" | sed ${sedopt} "s/\"([^\"]*)\",?/\1 /g" | tr "," "_"));
original_trans=($(echo "${content}" | cut -f 4 -d";" | sed ${sedopt} "s/(\[[^]]*\]),?/\1 /g"));
original_initials=($(echo "${content}" | cut -f 5 -d";" | sed ${sedopt} "s/\"([^\"]*)\",?/\1 /g" | tr "," "_"));
original_finals=($(echo "${content}" | cut -f 6 -d";" | sed ${sedopt} "s/\"([^\"]*)\",?/\1 /g" | tr "," "_"));

[ ${#original_initials[@]} -ne 1 ] && echo "Invalid initial state";

for t in "${original_trans[@]}"; do
  tmp=$(echo $t | sed "s/^\[\"\(.*\)\",\"\(.*\)\",\"\(.*\)\"\]$/\1;\2;\3/" | tr "," "_");

  from=$(echo "${tmp}" | cut -f 1 -d";");
  symbol=$(echo "${tmp}" | cut -f 2 -d";");
  to=$(echo "${tmp}" | cut -f 3 -d";");

  set_transition "original" "${from}" "${symbol}" "${to}";
done

complete_afd "original";
#to_dot "original";
#clear_afd "original";

G0=()
G1=()
for s in "${original_states[@]}"; do
  contains_in "$s" "${original_finals[@]}";
  if [ $? -eq 0 ]; then
    G1[${#G1[@]}]="${s}";
  else
    G0[${#G0[@]}]="${s}";
  fi
done

groups=2;
if [ ${#G0[@]} -eq 0 ]; then
  G0=(${G1[@]});
  unset G1;
  ((groups--));
elif [ ${#G1[@]} -eq 0 ]; then
  unset G1;
  ((groups--));
fi
[ ${#G0[@]} -eq 0 ] && fatal "No groups";

while true; do
  # Print the groups
  #for ((g = 0; g < groups; g++)); do
  #  eval echo "G${g}: \${G${g}[@]}";
  #done
  #echo "-------";

  # Build the table.
  tmp_states=(${original_states[@]});
  tmp_alphabet=(${original_alphabet[@]});
  for s in ${original_states[@]}; do
    for a in ${original_alphabet[@]}; do
      v=$(get_transition original "$s" "$a");

      for ((g = 0; g < groups; g++)); do
        eval contains_in "$v" "\${G${g}[@]}";
        [ $? -eq 0 ] && break;
      done
      [ $g -ge ${groups} ] && fatal "Not found";

      set_transition "tmp" "${s}" "${a}" "G${g}";
    done
  done

  # Build the new groups
  new_g=0;
  for ((g = 0; g < groups; g++)); do
    size=$(eval echo \${#G${g}[@]});
    while [ ${size} -gt 0 ]; do
      c=$(eval echo \${G${g}[0]});

      eval new_G${new_g}[\${#new_G${new_g}[@]}]=${c};
      eval unset G${g}[0];

      for ((i = 1; i < size; i++)); do
        c2=$(eval echo \${G${g}[i]});

        match=1;
        for a in ${original_alphabet[@]}; do
          target1=$(get_transition "tmp" "${c}" "${a}");
          [ -z "$target1" ] && fatal "Invalid transition";
          target2=$(get_transition "tmp" "${c2}" "${a}");
          [ -z "$target2" ] && fatal "Invalid transition";

          if [ "${target1}" != "${target2}" ]; then
            match=0;
            break;
          fi
        done

        if [ ${match} -eq 1 ]; then
          eval new_G${new_g}[\${#new_G${new_g}[@]}]=${c2};
          eval unset G${g}[i];
        fi
      done

      ((new_g++));
      eval "G${g}=(\${G${g}[@]})"
      size=$(eval echo \${#G${g}[@]});
    done
  done

  new_groups=${new_g};
  for ((new_g = 0; new_g < new_groups; new_g++)); do
    eval "unset G${new_g}";
    eval "G${new_g}=(\${new_G${new_g}[@]})";
    eval "unset new_G${new_g}";
  done

  [ ${new_groups} -eq ${groups} ] && break;
  groups=${new_groups};

  clear_afd "tmp";
done

min_states=();
min_alphabet=(${original_alphabet[@]});
min_initials=()
min_finals=()

for ((g = 0; g < groups; g++)); do
  min_states[${#min_states[@]}]="G${g}";

  eval "contains_in ${original_initials[0]} \${G${g}[@]}";
  if [ $? -eq 0 ]; then
    min_initials[0]="G${g}";
  fi

  x=$(eval "echo \${G${g}[0]}");
  contains_in ${x} ${original_finals[@]};
  if [ $? -eq 0 ]; then
    min_finals[${#min_finals[@]}]="G${g}";
  fi

  for a in ${min_alphabet[@]}; do
    t=$(get_transition "tmp" "${x}" "${a}");
    [ -z "${t}" ] && fatal "Invalid transition";

    set_transition "min" "G${g}" "${a}" "${t}";
  done
done

to_dot "min";
clear_afd "min";