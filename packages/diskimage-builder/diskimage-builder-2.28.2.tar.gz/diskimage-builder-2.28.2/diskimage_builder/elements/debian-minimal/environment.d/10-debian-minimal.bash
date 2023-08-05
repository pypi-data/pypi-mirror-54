export DISTRO_NAME=debian
export DIB_RELEASE=${DIB_RELEASE:-stable}

if [ -n "${DIB_DEBIAN_DISTRIBUTION_MIRROR:-}" ]; then
    DIB_DISTRIBUTION_MIRROR=$DIB_DEBIAN_DISTRIBUTION_MIRROR
fi
export DIB_DISTRIBUTION_MIRROR=${DIB_DISTRIBUTION_MIRROR:-http://deb.debian.org/debian}

# With Debian, security is in a different repository.  We can't, say,
# assume "${DIB_DISTRIBUTION_MIRROR}-security" is valid.  The only
# choice is for people to add it separately, otherwise we use
# upstream.
DIB_DEBIAN_SECURITY_MIRROR=${DIB_DEBIAN_SECURITY_MIRROR:-http://security.debian.org/}

export DIB_DEBIAN_COMPONENTS=${DIB_DEBIAN_COMPONENTS:-main}
export DIB_DEBIAN_COMPONENTS_WS=${DIB_DEBIAN_COMPONENTS//,/ }

DIB_APT_SOURCES_CONF_DEFAULT=\
"default:deb ${DIB_DISTRIBUTION_MIRROR} ${DIB_RELEASE} ${DIB_DEBIAN_COMPONENTS_WS}
backports:deb ${DIB_DISTRIBUTION_MIRROR} ${DIB_RELEASE}-backports ${DIB_DEBIAN_COMPONENTS_WS}
updates:deb ${DIB_DISTRIBUTION_MIRROR} ${DIB_RELEASE}-updates ${DIB_DEBIAN_COMPONENTS_WS}
security:deb ${DIB_DEBIAN_SECURITY_MIRROR} ${DIB_RELEASE}/updates ${DIB_DEBIAN_COMPONENTS_WS}
"

if [ "${DIB_RELEASE}" = "testing" -o "${DIB_RELEASE}" = "unstable" ]; then
    DIB_APT_SOURCES_CONF_DEFAULT="default:deb ${DIB_DISTRIBUTION_MIRROR} ${DIB_RELEASE} ${DIB_DEBIAN_COMPONENTS_WS}"
fi

export DIB_APT_SOURCES_CONF=${DIB_APT_SOURCES_CONF:-${DIB_APT_SOURCES_CONF_DEFAULT}}
