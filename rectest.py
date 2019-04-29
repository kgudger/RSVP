import obspython as obs
import subprocess
# Python script for OBS control of the blink(1) light

source_name = ""

def script_update(settings):
	global source_name

	source_name = obs.obs_data_get_string(settings, "source")

def script_properties():
	props = obs.obs_properties_create()

	p = obs.obs_properties_add_list(props, "source", "Text Source", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
	sources = obs.obs_enum_sources()
	if sources is not None:
		for source in sources:
			source_id = obs.obs_source_get_id(source)
			if source_id == "text_gdiplus" or source_id == "text_ft2_source":
				name = obs.obs_source_get_name(source)
				obs.obs_property_list_add_string(p, name, name)

		obs.source_list_release(sources)

	return props

def cb_recording(text):
	def cb(callback_data):
		code = obs.calldata_int(callback_data, "code")

		if ( text == "start" ):
			rv = subprocess.call("C:\\Users\\Editor\\Desktop\\blink1-tool.exe --red -m 0")
		else:
			rv = subprocess.call("C:\\Users\\Editor\\Desktop\\blink1-tool.exe --blue -m 0")
		print("Return value = " + str(rv))
		return True
	return cb

def script_load(settings):
	handler = obs.obs_output_get_signal_handler(obs.obs_frontend_get_recording_output())
	obs.signal_handler_connect(handler, "start", cb_recording("start"))
	obs.signal_handler_connect(handler, "stop", cb_recording("stop"))

# set default color for light before starting
rv = subprocess.call("C:\\Users\\Editor\\Desktop\\blink1-tool.exe --blue -m 0")
print("Return value = " + str(rv))


