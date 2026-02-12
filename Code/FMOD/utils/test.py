class Tmp:
    def submit(self, wert):
        print(wert)


nombre: Tmp = Tmp()
alter: Tmp = Tmp()
wohnort: Tmp = Tmp()

old_vals:dict = {"name": "JJ", "alter": 13, "wohnort": "Mecktwn"}
new_vals:dict = {"name": "JJ", "alter": 21, "wohnort": "Nürne"}

common_keys = old_vals.keys() & new_vals.keys()

diff = {k: (k, v) for k, v in new_vals.items()
    if old_vals.get(k) != v}

actions = {
    "name": nombre,
    "alter": alter,
    "wohnort": wohnort
}

for k in diff.keys():
    actions[k].submit(diff[k])
