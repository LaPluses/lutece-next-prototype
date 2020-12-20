import asyncio
import argparse
import pathlib
import re

# Event mask defination, ref to http://emcrisostomo.github.io/fswatch/doc/1.7.0/fswatch.html/Invoking-fswatch.html#Custom-Record-Formats
PLATFORM_SPECIFIC = 1 << 0
CREATED = 1 << 1
UPDATED = 1 << 2
REMOVED = 1 << 3
RENAMED = 1 << 4
OWNER_MODIFIED = 1 << 5
ATTRIBUTE_MODIFIED = 1 << 6
MOVED_FROM = 1 << 7
MOVED_TO = 1 << 8
IS_FILE = 1 << 9
IS_DIR = 1 << 10
IS_SYM_LINK = 1 << 11
LINK = 1 << 12
OVER_FLOW = 1 << 13

# Const varibles
DIR = pathlib.Path(__file__).parent.absolute()
MAKEFILE = pathlib.Path.joinpath(DIR, "makefile")
PROTO_FS_CMD = f'fswatch -n -x -r -l 1 {DIR}/proto'

# Argument parser defination
parser = argparse.ArgumentParser(
    description="Lutece next bootstrap programme", allow_abbrev=False
)

parser.add_argument(
    "-debug",
    "-d",
    action="store_true",
    default=False,
    help="Enable debug",
    dest="debug",
)

parser.add_argument(
    "-disable_proto_watcher",
    action="store_true",
    default=False,
    help="Disable proto hotswap",
    dest="disable_proto_watcher",
)

# Log defination
class Log:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    @staticmethod
    def info(msg):
        print(f"{Log.OKCYAN}[INFO]: {msg}{Log.ENDC}")

    @staticmethod
    def error(msg):
        print(f"{Log.FAIL}[ERROR]: {msg}{Log.ENDC}")

    @staticmethod
    def is_debug_then_info(msg):
        if args.debug:
            print(f"{Log.OKCYAN}[INFO]: {msg}{Log.ENDC}")

    @staticmethod
    def plain(msg):
        print(f"{msg}")
    

def get_handler(
    cmd, delay, before=None, after=None, ok_callback=None, err_callback=None
):
    execution = False

    async def handle_func():
        nonlocal execution
        execution = True
        await asyncio.sleep(delay)
        if not execution:
            return
        execution = False
        if before:
            before()
        proc = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        if not proc.returncode and ok_callback:
            ok_callback()
        if stderr and err_callback:
            err_callback(stderr.decode())
        if after:
            after()

    return handle_func


def is_file_change(event_code):
    return (event_code >> CREATED & 1) | \
           (event_code >> UPDATED & 1) | \
           (event_code >> REMOVED & 1) | \
           (event_code >> RENAMED & 1)

def extension_check(s,extension):
    if re.search( f'.*\.{extension}$' , s):
        return True
    return False

async def add_err_watcher(proc, msg):
    err = await proc.stderr.read()
    Log.error(msg)
    Log.plain(err)
    proc.kill()

async def add_proto_watcher(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    handle_func = get_handler(
        f"make -f {MAKEFILE} gen_proto",
        2,
        ok_callback=lambda: Log.info(f"proto hotswap done"),
        err_callback=lambda err: Log.error(f"Error on proto compile\n {err}"),
    )
    asyncio.create_task(add_err_watcher(proc, "Proto fswatch error happen"))
    while True:
        output = await proc.stdout.readline()
        fs, status_code = output.decode().split(" ")
        status_code = int(status_code)
        if extension_check(fs, 'proto') and is_file_change(status_code):
            Log.is_debug_then_info(
                f"detect file change, schedule one proto modification operation"
            )
            asyncio.create_task(handle_func())
 
async def main():
    Log.info('Bootstrap program started')
    task = []
    if args.debug:
        Log.info('* Debug mode enabled')
    if args.disable_proto_watcher:
        Log.info('* Proto watcher disabled')
    else:
        Log.info('* Start proto watcher')
        task.append( asyncio.create_task(add_proto_watcher(PROTO_FS_CMD)) )
    if len(task) > 0:
        await asyncio.wait(task)
    Log.info('Bootstrap program done')

args = parser.parse_args()
asyncio.run(main())