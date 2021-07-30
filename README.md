# Secbox

TODO: description

- [Installation](#installation)
  - [OpenSUSE](#OpenSUSE-Leap-15.2--15.3--Tumbleweed)
  - [Git](#Git)
- [Configuration](#configuration)
  - [Aliases](#Enable-secbox-via-aliases)
  - [Network resources](#Ensure-network-resources-access)
- [Test it](#test-it)
- [Want to know more?](#want-to-know-more)
  - [Why](#why)
  - [Components](#Components)
  - [Break it](#Break-it-Dont-be-afraid,-it's-just-a-container)
  - [Reset button](#Reset-button)
  - [Make permanent changes](#Make-permanent-changes)
  - [Use of the mount options](#Use-of-the-mount-options)

## Installation

 * OpenSUSE Leap 15.2 / 15.3 / Tumbleweed

        _opensuse_version=$(cat /etc/os-release | grep -Po "(?<=PRETTY_NAME=\").*(?=\")" | sed 's/ /_/g');
        zypper addrepo https://download.opensuse.org/repositories/security/${_opensuse_version}/security.repo && \
        zypper --non-interactive --gpg-auto-import-keys refresh && \
        zypper --non-interactive install -y secbox && \
        unset _opensuse_version

 * Git

        git clone https://github.com/StayPirate/secbox.git
        export PATH=$PATH:$(pwd)/secbox

## Configuration
 * ### **Enable secbox via aliases**

    Secbox is mainly executed through aliases. For instance, to run the containerized tool `osc`, you need to run `secbox osc`. A set of commonly used aliases are provided via the `--alias` cmdline option. This is meant to automatically load aliases by adding the following command to your favorite shell rc file. (Eg. `~/.bashrc` , `~/.zshrc`)

        eval "$(secbox --alias)"

    This way if new aliases are added in an updated version of secbox, you will get automatically added without any action from your side. If you create more aliases don't be shy and submit them via a PR, I'll be glad to merge them.

 * ### **Ensure network resources access**

    In order to get some of the internal tools properly work, secbox needs to make some remote folders available on specific mountpoints. Secbox supports two different protocols for that:

   1. NFS  
      It can be triggered through the option `--nfs`, since mounting requires high privileges your user's passoword would be asked to try to escalate them and mount required nfs exports. A list of mounted exports is maintained within the [`nfs_shares` array](https://github.com/StayPirate/secbox/blob/master/secbox#L97-L107).

   2. SSHFS *(prefered)*  
      A **better approach** is the `--sshfs` option. Secbox can use sshfs (no need to install sshfs in your host) to mount `wotan.suse.de:/mounts` in the right place within the container. In order to make this option works you need to configure your host to be able to access wotan just by running `ssh wotan`. That's can easily be accomplished throught a proper configured `~/.ssh/config`. If you have not yet configured your, then you could use the following stanza template:

          Host wotan
              HostName wotan.suse.de
              User <YOUR_USERNAME>
              PreferredAuthentications publickey
              IdentityFile /path/to/your/key

      In case you manage your ssh keys with the ssh-agent you can avoid the last line (IdentityFile) since secbox will automatically use ssh-agent to authenticate.

      To check if your ssh setup is correct, try to access wotan issuing the command `ssh wotan`, you should get similar results:

            host> ssh wotan
            Last login: Fri Jul 30 06:32:42 2021 from 2620:113:80c0:8340::11f1
            This machine is used as:
            * ...
            * ...
            * ...
            * ...

            Feel free to have a look into our configuration files in /etc

            Questions/Remarks? Please sent a mail to xxx@email.com.
            Issues, please open a ticket by sending an email to xxx@email.com.

            Have a lot of fun...

            <YOUR_USERNAME>@wotan:~>

## Test it

If you manage to take all the above steps you should now be able to use secbox! First of all, ensure your shell rc-script has been re-sourced (open a new shell, manually source it, or manually run `eval "$(secbox --alias)"`).

Now it's time to check if scebox works as expected. Run `secbox echo Hello outside world, I\'m running inside the container.`

    host> secbox echo Hello outside world, I\'m running inside the container.
    Hello outside world, I'm running inside the container.


Since this is your first time running secbox, then the container will be automatically created, hence you will see some extra output.

Keep in mind that well-designed containers are [ephemeral](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#create-ephemeral-containers), and that's the case of [secbox-image](https://gitlab.suse.de/security/secbox-image), the container image under the secbox's hood. That's mean that you're free to destroy/replace the container at your will, nothing will change from your point of view. To make it easy you can use `secbox --destroy` to delete the currently running container.

Last but not least, don't forget `secbox --help` is your friend.

## Want to know more?

 * ### Why?

    Let's start from the beginning, when I joint the security team I've been told to use several home-made tools to accomplish my daily tasks, these tools are a huge varaity of scripts written in many different languages and hosted all together in a common git repository. To be honest I didn't like that and I definetely didn't like the idea of cloning that repo and put its path in my $PATH. Even if I would have done that, it wouldn't been enough... In order to make those scripts working, all the dependencies were required to be manually resolved everytime an error was hit. *Ça va sans dire* the documentation were almost not existing, but luckly the SUSE security team is a really great place to work in and each team-mate is super willing to help and answer any question. In order to have an easier to maintain setup my idea was to manage a container image in a VCS fashion (git) containing all the required tools and related dependencies and I wanted make it usuable in a trasparent way, I would have worked exaclty as any other team-mate who installed those tools on his host system. Moreover, I was the only one not yet using openSUSE as host operating system and many of these custom scripts only work if ran within a SUSE-based OS... so I really needed a container to have the required OS layout below.

 * ### Components

    Secbox is composed by two pieces, `secbox` and `secbox-image`.

     * `secbox` is the software you can find in this repository and it's the **only thing** you have to take care of install, configure and use. It's written in bash because portability is an hard-requirement for me. If you check my [dotfiles](https://github.com/StayPirate/dotfiles) out you can undestand how much I care about portability.

     * `secbox-image` is the container image where all the needed tools and related dependencies are installed, its also easy to maintain with git since it's just a Dockerfile. In contrast of secbox, it's hosted in our internal [gitlab instance](https://gitlab.suse.de/security/secbox-image), not in GitHub. The reason is because there is a CI/CD pipeline which instructs IBS to rebuild the image at each new tag-push and publish it to our internal [registry](https://registry.suse.de). I'd love to use GitHub actions instead, but some of the rpms installed at build-phase are in private repositories :(, and only IBS does have access to them.
 * ### Break it! (Don't be afraid, it's just a container)

    As I mentioned above, [secbox-image](https://gitlab.suse.de/security/secbox-image) is designed to create [ephemeral](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#create-ephemeral-containers) containers. You are free to mess the container up, destroy, create it again and keep working as usual.

    First of all, let's see how to get inside the container:

        host> secbox bash
        [crazybyte@wintermute ~]$ echo I\'m in
        I'm in

    Quite easy, right? If you play a little bit with a shell inside the container you will quickly realize you're still the same user as in your host system and you still see the same undeline filesystem (what?)

        host> id; pwd
        uid=1000(crazybyte) gid=1001(crazybyte) groups=1001(crazybyte),1000(autologin)
        /home/crazybyte
        host> secbox bash
        [crazybyte@wintermute ~]$ id; pwd
        uid=1000(crazybyte) gid=1001(crazybyte) groups=1001(crazybyte)
        /home/crazybyte

    That's a very important thing to understand while using `secbox`. It creates a namespace where the current rootless user's UID:GID maps to the same values in the container. When the container is launched, **it is running as your UID inside the container and on the host**. Moreover, **your user's home and temporary folders are mounted as volumes**. That means even if `secbox` runs everything inside a container, there **are NOT the same security bundaries** as you'll get with isolated namespaces. Of course, it's a rootless container so highest level of demage you could achieve is the same as from your host user. Your home folder is shared, hence all the contained files can be read/deleted/changed (if your host user has rw permissions on them). Secbox makes your life easier since it simplify your setup, increase the portability and everybody in the team can share the same setup state. Below I describe how to change your container and make this change available to the rest of the team via the container update process.

    Inside the container you are in an openSUSE-based OS, so zypper is available. Let's try it!

        host> secbox bash
        [crazybyte@wintermute ~]$ zypper install cowsay
        Root privileges are required to run this command.

    Interesting, we can't obviuslly perform any privileged task inside the container since it's a rootless container. But I would like to install new things, make some changes, customize this container. Secbox can help you with that, let's try to run it with the `--root` flag.

        host> secbox --root

            !!!                            ~ Be CaReFuL ~                             !!!
            !!!  secbox is a rootless container, that means this root user is mapped  !!!
            !!!  with your host crazybyte account. While you can install any package  !!!
            !!!  or change any container's file, DO NOT FORGET that your host-user's  !!!
            !!!  HOME directory is shared with this container. Any change performed   !!!
            !!!  in /home/crazybyte is reflected to your host filesystem.             !!!
            !!!  In case you messed up the container, DON'T PANIC! Just destroy and   !!!
            !!!  recreate it 'secbox --destroy' and 'secbox echo Hello World'         !!!
            !!!                            ~ Be CaReFuL ~                             !!!

        wintermute:/home/crazybyte # zypper install cowsay
        Loading repository data...
        Reading installed packages...
        Resolving package dependencies...

        The following NEW package is going to be installed:
        cowsay

        1 new package to install.
        Overall download size: 26.2 KiB. Already cached: 0 B. After the operation, additional 29.1 KiB will be used.
        Continue? [y/n/v/...? shows all options] (y): y
        Retrieving package cowsay-3.03-lp152.3.3.noarch                        (1/1),  26.2 KiB ( 29.1 KiB unpacked)
        Retrieving: cowsay-3.03-lp152.3.3.noarch.rpm ............................................[done (90.3 KiB/s)]

        Checking for file conflicts: .........................................................................[done]
        (1/1) Installing: cowsay-3.03-lp152.3.3.noarch .......................................................[done]

        wintermute:/home/crazybyte # cowsay -f ghostbusters There\'s no ghost in this shell, yet.
         --------------------------------------
        < There's no ghost in this shell, yet. >
         --------------------------------------
                  \
                   \
                    \          __---__
                            _-       /--______
                       __--( /     \ )XXXXXXXXXXX\v.
                     .-XXX(   O   O  )XXXXXXXXXXXXXXX-
                    /XXX(       U     )        XXXXXXX\
                  /XXXXX(              )--_  XXXXXXXXXXX\
                 /XXXXX/ (      O     )   XXXXXX   \XXXXX\
                 XXXXX/   /            XXXXXX   \__ \XXXXX
                 XXXXXX__/          XXXXXX         \__---->
         ---___  XXX__/          XXXXXX      \__         /
           \-  --__/   ___/\  XXXXXX            /  ___--/=
            \-\    ___/    XXXXXX              '--- XXXXXX
               \-\/XXX\ XXXXXX                      /XXXXX
                 \XXXXXXXXX   \                    /XXXXX/
                  \XXXXXX      >                 _/XXXXX/
                    \XXXXX--__/              __-- XXXX/
                     -XXXXXXXX---------------  XXXXXX-
                        \XXXXXXXXXXXXXXXXXXXXXXXXXX/
                          ""VXXXXXXXXXXXXXXXXXXV""

    DON'T PANIC this root account inside the container is not mapped to the root user in the host. You can do whaterver you want inside the container, but on the host system you can only achieve the same demage level as if you run secbox without the `--root` flag (see above).

 * ### Reset button

    Any change you did while inside the container (except for files in mounted voulmes) can be reverted just by deleting and recreating the container. The container will be automatically recreated at the next secbox run, and everything will be back to normal (whatever the normality is).

        host> secbox --destroy
                        _
            ___ ___ ___| |_ ___ _ _
           |_ -| -_|  _| . | . |_'_|
           |___|___|___|___|___|_,_|

        [.] Do you really want to destroy secbox [y/N] y
        [.] container stopped
        [.] container autostart disabled
        [.] secbox container deleted
        host> secbox bash
                        _
            ___ ___ ___| |_ ___ _ _
           |_ -| -_|  _| . | . |_'_|
           |___|___|___|___|___|_,_|

        [*] secbox container not found
        [.] secbox container created

        [crazybyte@wintermute ~]$ cowsay "To be, or not to be, that is the question."
        bash: cowsay: command not found

    It seems the cow can't say anything anymore, any existential question is over.

    Of course, if `cowsay` is still installed inside the container, you can use it without entering into the container shell all the time. That's ascutally the strainght of secbox! Just run like this:

        host> secbox cowsay Hi folks
         ----------
        < Hi folks >
         ----------
                \   ^__^
                 \  (oo)\_______
                    (__)\       )\/\
                        ||----w |
                        ||     ||

    The next step is to create an alias in the host, to use cowsay as it was installed inside the host system.

        host> alias cowsay='secbox cowsay'
        host> cowsay Hi folks
         ----------
        < Hi folks >
         ----------
                \   ^__^
                 \  (oo)\_______
                    (__)\       )\/\
                        ||----w |
                        ||     ||

    I really hope this exaple helped you to understand how all the tools are used in `secbox`. The tools `osc` for the host is just `secbox osc`, and this alias is loaded when `​eval "$(secbox --alias)"` is executed inside your shell.


 * ### Make permanent changes

    Now that you know how to customize your container, you don't have to forget that **any change you done in a live container will only last until that container is destroyed**.

    TODO

 * ### Use of the mount options

    If you are wondering why there is not one but two way to automatically mount network resources, then keep reading.

    TODO