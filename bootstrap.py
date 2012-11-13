import sys
import os

# NOTE: You need to have a version of The AI Sandbox that matches this SDK
# version number.  More recent versions of The AI Sandbox may work, but
# ideally you should use the update scripts or grab the newest versions
# from the http://aisandbox.com/ homepage.

SBX_REQUIRED_VERSION = "0.20.1"


def find_eggs(path):
    """Scan the specified directory for packaged EGG modules, and add them
    to the Python path so they can be imported as any other module."""

    for folder, subs, files in os.walk(path):
        for filename in [f for f in files if f.endswith('.egg')]:
            path = os.path.join(folder, filename)
            sys.path.append(os.path.abspath(path))


def setup_paths(binaryDir):
    """Given a binary directory, add necessary paths to the Python system for
    importing modules and egg files."""

    paths = [
        binaryDir,
        os.path.join(binaryDir, 'lib'),
        os.path.join(binaryDir, 'scripts'),
    ]
    sys.path.extend([os.path.normpath(p) for p in paths])

    find_eggs(paths[0])
    find_eggs(sys.path[0])


def setup_directory(workDir):
    """Knowing the working directory, make sure this is active and tell the
    AI Sandbox module of the starting directory to find various data files."""

    os.chdir(os.path.join(workDir, 'binaries'))

    from aigd import ApplicationFramework
    ApplicationFramework.setInitialDirectory(os.path.join(sys.path[0], ''))


def setup_version(requiredVersion):
    """Knowing the required version of The AI Sandbox, check if it's there and
    perform and update if necessary."""

    if not requiredVersion:
        return

    try:        
        from aisbx import version            
        if version.checkValid(requiredVersion):
            return
        else:        
            version.doUpdate()

    except ImportError:
        print >>sys.stderr, 'Error initializing The AI Sandbox version %s.  Starting update...' % requiredVersion
        
        import subprocess
        subprocess.call(['update.exe'], cwd = os.path.join('%LocalAppData%', 'AiGameDev.com', 'The AI Sandbox'), shell = True)
    except:
        print >>sys.stderr, 'Fatal error initializing The AI Sandbox version %s!  Please update.' % requiredVersion
        import traceback
        print >>sys.stderr, ' '.join(traceback.format_exception(*sys.exc_info()))
    
    sys.exit(-1)


def initialize():
    """The main entry point of the bootstrap module, used to setup everything from paths to
    working directories and platform versions."""

    if '-devpath' in sys.argv:
        sys.argv.remove('-devpath')
        SBX_WORKING_DIR = os.path.split(os.getcwd())[0]
        SBX_BINARY_DIR = os.path.join(SBX_WORKING_DIR, 'binaries')
        sys.path.append(os.path.join('..', 'source', 'platform'))
    else:
        SBX_WORKING_DIR = os.environ.get('AISANDBOX_DIR', ".")
        SBX_BINARY_DIR = os.environ.get('AISANDBOX_BIN', ".")		

    setup_paths(SBX_BINARY_DIR)
    setup_directory(SBX_WORKING_DIR)
    setup_version(SBX_REQUIRED_VERSION)

initialize()
