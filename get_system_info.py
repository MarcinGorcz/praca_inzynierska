import psutil
import platform

#TODO: To odpala sie na komputerze uzytkownika.
#TODO: Kto to ma odpalac?
#TODO: Jak ma byc przekazywana informacja do bazy danych? Jakis server/klient do nadpisywania?
#TODO: Jak czesto update?
#TODO: Warto to w ogole robic? Moze lepiej wlaczyc raz i przekazac informacje poza systemem podczas rejestracji?

class parametry_komputera:
    def __init__(self):
        uname = platform.uname()

        #SYSTEM
        self.system_operacyjny = uname.system
        self.wersja_systemu = uname.version

        #CPU
        cpufreq = psutil.cpu_freq()
        self.rdzenie_fizyczne = psutil.cpu_count(logical=False)
        self.rdzenie_logiczne = psutil.cpu_count(logical=True)
        self.cpufreq = cpufreq.min

        #RAM
        svmem = psutil.virtual_memory()
        self.ram = svmem.total

        #Pamiec
        self.dyski = {}
        for partition in psutil.disk_partitions():
            self.dyski[str(partition.device)] = psutil.disk_usage(partition.mountpoint).used
            #partition_usage.total
        #PODSUMOWANIE:
        self.tabela_systemu = {
            "SystemOperacyjny":self.system_operacyjny,
            "WersjaSystemu":self.wersja_systemu,
            "IloscRdzeniFizycznych":self.rdzenie_fizyczne,
            "IloscRdzeniLogicznych":self.rdzenie_logiczne,
            "TaktowanieRdzeni":self.cpufreq,
            "IloscRamu":self.ram,
            "Dyski":self.dyski,
        }

    def dopasuj_maszynę(self):
        typy_tl = [
            {"type" : "e2-standard-2","cpu": 2, "memory": 8},
            {"type" : "e2-standard-4","cpu": 4, "memory": 16},
            {"type" : "e2-standard-8","cpu": 8, "memory": 32},
            {"type" : "e2-standard-16","cpu": 16, "memory": 64},
            {"type" : "e2-standard-32","cpu": 32, "memory": 128},
        ]
        ram = self.tabela_systemu["IloscRamu"]/(1024*1024*1024)
        cpu = 1
        #cpu = self.tabela_systemu["IloscRdzeniLogicznych"]
        wybrany_typ=""

        for tl in typy_tl:
            if(int(tl["cpu"])>int(cpu) and float(tl["memory"])>float(ram)):
                wybrany_typ = tl["type"]
                break
        if(wybrany_typ == ""):
            wybrany_typ= "e2-standard-32"
        self.tabela_systemu["ZalecanyVM"] = wybrany_typ
        print(wybrany_typ)

    def printuj_system(self):
        print(self.tabela_systemu)

    def konwertuj_do_VHD(self):
        if(self.tabela_systemu == "Windows"):
            pass
        if(self.tabela_systemu == "Linux"):
            pass
        else:
            raise Exception("Sorry your system is not supported")
        pass


Linux = parametry_komputera()
Linux.printuj_system()
Linux.dopasuj_maszynę()