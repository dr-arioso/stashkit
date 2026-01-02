from stashkit.stashbench import StashBench

class DataQuerySkill:
    def run(self, *, query_packet=None, **_):
        if query_packet is None:
            return {"help_me": "no_querypacket"}

        try:
            raw = StashBench.data.connection(query_packet)
        except Exception as e:
            return {"help_me": str(e)}

        # no mapping yet
        return {"raw": raw}

qp = {
    "connection": {
        "endpoint": "https://example.com/api",
 #       "protocol": "http_json",
    },
    "inputs": {
        "upc_code": "code"
    }
}

#result = StashBench.data.connection({
#    "connection": {"endpoint": "x"}
#})

result = DataQuerySkill(qp)

print(result)



# Experiment #1:
# Yeah, those error message feel right.
# Don't feel the need to add anything else now

# Experiment #2:
# Empty dict results in: ValueError: QueryPacket missing 'connection' section
# Sending only connection.endpoint results in: ValueError: QueryPacket missing connection.protocol
# They do point to what should be supplied next.
# Sort of feels like it should specify everything it's missing. Maybe overkill.
# Dunno if they'd map cleanly to a help_me; dunno if they'd need to (since that means that the skill is asking for somebody else to do something. I dunno. Could.

# Experiment #3:
# This shouldn't ever go though, right? Because DataQuerySkill's SkillDescriptor.requires includes a 
'''
(venv) PS C:\Users\billj\Dropbox\Bill's stuff\Coding\GitHub\StashKit\tests> python -m tester
Traceback (most recent call last):
  File "C:\Users\billj\AppData\Local\Programs\Python\Python310\lib\runpy.py", line 196, in _run_module_as_main
    return _run_code(code, main_globals, None,
  File "C:\Users\billj\AppData\Local\Programs\Python\Python310\lib\runpy.py", line 86, in _run_code
    exec(code, run_globals)
  File "C:\Users\billj\Dropbox\Bill's stuff\Coding\GitHub\StashKit\tests\tester.py", line 30, in <module>
    result = DataQuerySkill(qp)
TypeError: DataQuerySkill() takes no arguments
'''
# Experiment #4:
# maybe reliability (distinctive from confidence)

