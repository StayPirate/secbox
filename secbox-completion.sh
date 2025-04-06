# Bash completion for secbox
# 2022 Filippo Bonazzi (filippo dot bonazzi at suse dot com)

_generate_secbox_cmds_file()
{
  # Check that we have the output folder parameter
  if [ "$#" -ne 1 ]
  then
    >&2 echo "usage: ${FUNCNAME[0]} <OUT_FOLDER>"
    return 1
  fi

  # Check if output directory exists and is writeable
  if [[ -d "$1" ]] && [[ -x "$1" ]] && [[ -w "$1" ]]
  then
    secbox bash -c "compgen -c" > "$1/secbox_cmds.lst"
  else
    >&2 echo "Bad folder: $1"
    >&2 echo "usage: ${FUNCNAME[0]} <OUT_FOLDER>"
    return 1
  fi
}

_secbox_completion()
{
  local cur prev opts

  COMPREPLY=()
  cur="${COMP_WORDS[COMP_CWORD]}"
  prev="${COMP_WORDS[COMP_CWORD-1]}"

    # Get list of commands available in secbox from file
    # TODO: how do we find the file?
    cmds=$(tr '\n' ' ' < secbox_cmds.lst)

    opts="--sshfs --nfs --destroy --root --debug --update-container --no-color --alias --tty --no-tty --interactive --no-interactive -h --help -v --version"

    # If we are completing the first time, complete on commands and options
    if [[ $COMP_CWORD -eq 1 ]]
    then
      COMPREPLY=( $( compgen -W "$cmds $opts" -- "$cur" ) )
      return 0
    fi

    # Otherwise complete with more context
    case "$prev" in
      --destroy)
        COMPREPLY=( $( compgen -W '-i -f' -- "$cur" ) )
        ;;
      --update-container)
        COMPREPLY=( $( compgen -W '-f --force' -- "$cur" ) )
        ;;
      -*)
        COMPREPLY=( $( compgen -W "$opts" -- "$cur" ) )
        ;;
    esac

  }

# Use _secbox_completion to generate completion for secbox
complete -F _secbox_completion secbox
