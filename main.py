import os
import asyncio
import aiohttp
from sys import stdout
from time import sleep
from utils import Utils
from datetime import datetime
from colorama import Fore, Style
from proxymanager import ProxyManager

working = 0
task_queue = asyncio.Queue()
current_directory = os.getcwd()
date = datetime.now().strftime("%Y_%m_%d-%I-%M-%S_%p")

async def counter(value):
    global working
    if "working" in value.lower():
        working += 1

    stdout.write(
    f"\x1b]2;Proxy Checker by Jag | "
    f"Working {working}/{proxyqty}\x07")

async def start(threads):
    global proxyqty
    proxyqty = task_queue.qsize()
    tasks = []
    for i in range(threads):
        i += 1
        task = asyncio.create_task(ProxyChecker(i).tasks())
        tasks.append(task)

    await asyncio.gather(*tasks)

class ProxyChecker():
    
    def __init__(self, task_id):
        self.task_id = f"[Task {task_id}]"
    
    async def tasks(self):
        while True:
            if not task_queue.empty():
                proxy = task_queue.get_nowait()
                async with aiohttp.ClientSession() as session:
                    await self.check(proxy, session)
                task_queue.task_done()
                await session.close()
            else:
                pass

    async def check(self, proxy, session):
        while True:
            try:
                await session.head("https://www.supremenewyork.com", proxy = f"http://{ProxyManager.parse_proxy_string(proxy)}", timeout = 15)
                await counter("working")
                print(f"{Fore.CYAN}{Style.BRIGHT}{self.task_id} Proxy Working - {proxy}{Style.RESET_ALL}")
                with open(f"{current_directory}\\output\\working_{date}.txt","a+") as outputfile:
                    print(proxy, file=outputfile)
                return
            except Exception:
                print(f"{Fore.RED}{Style.BRIGHT}{self.task_id} Proxy Not Working - {proxy}{Style.RESET_ALL}")
                return

if __name__ == "__main__":

    Utils.title()
    Utils.clear()

    try:
        os.makedirs(f"{current_directory}\\output", exist_ok=True)
    except Exception:
        Utils.clear()
        print(f"{Fore.RED}Error making output folder{Style.RESET_ALL}")
        sleep(2)
        os._exit(1)

    try:
        print(f"{Fore.CYAN}{Style.BRIGHT}PROXIES{Fore.WHITE}{Style.RESET_ALL}")
        proxyFiles = os.listdir(f"{current_directory}\\proxies")
        proxylist = []
        fileno = 0
        for file in proxyFiles:
            if file.endswith(".txt"):
                fileno+=1
                filename = os.path.join(file)
                proxylist.append(filename)
                print(f"[{fileno}] {filename}")
        if fileno == 0:
            Utils.clear()
            print(f"{Fore.RED}Add proxy text file(s) into the proxies folder{Style.RESET_ALL}")
            sleep(2)
            os._exit(1)
    except Exception:
        Utils.clear()
        print(f"{Fore.RED}Error with proxy file(s){Style.RESET_ALL}")
        sleep(2)
        os._exit(1)

    while True:
        try:
            proxyInput = int(input(f"{Fore.MAGENTA}{Style.BRIGHT}\nPROXY INPUT\n{Fore.WHITE}{Style.RESET_ALL}"))
            if proxyInput > len(proxylist) or proxyInput < 1:
                print(f"{Fore.RED}INVALID INPUT{Style.RESET_ALL}")
            else:
                break
        except Exception:
            print(f"{Fore.RED}INVALID INPUT{Style.RESET_ALL}")

    try:
        proxyfile = proxylist[proxyInput-1]
        ProxyManager.load_queue(task_queue, f"{current_directory}\\proxies\\{proxyfile}")
    except Exception:
        Utils.clear()
        print(Fore.RED+"Error formatting proxy file(s)"+Style.RESET_ALL)
        sleep(2)
        os._exit(1)

    while True:
        try:
            runInput = int(input(f"{Fore.BLUE}\nTASK QUANTITY\n{Fore.WHITE}{Style.RESET_ALL}"))
            if runInput > 0:
                break
            else:
                print(f"{Fore.RED}INVALID INPUT{Style.RESET_ALL}")
        except Exception:
            print(f"{Fore.RED}INVALID INPUT{Style.RESET_ALL}")

    Utils.clear()

    asyncio.run(start(runInput))
