# modified from https://github.com/ThomasRinsma/pdftris
import cv2

PDF_FILE_TEMPLATE = """
%PDF-1.6

% Root
1 0 obj
<<
  /AcroForm <<
    /Fields [ ###FIELD_LIST### ]
  >>
  /Pages 2 0 R
  /OpenAction 17 0 R
  /Type /Catalog
>>
endobj

2 0 obj
<<
  /Count 1
  /Kids [
    16 0 R
  ]
  /Type /Pages
>>

%% Annots Page 1 (also used as overall fields list)
21 0 obj
[
  ###FIELD_LIST###
]
endobj

###FIELDS###

%% Page 1
16 0 obj
<<
  /Annots 21 0 R
  /Contents 3 0 R
  /CropBox [
    0.0
    0.0
    612.0
    792.0
  ]
  /MediaBox [
    0.0
    0.0
    612.0
    792.0
  ]
  /Parent 2 0 R
  /Resources <<
  >>
  /Rotate 0
  /Type /Page
>>
endobj

3 0 obj
<< >>
stream
endstream
endobj

17 0 obj
<<
  /JS 42 0 R
  /S /JavaScript
>>
endobj


42 0 obj
<< >>
stream

// Hacky wrapper to work with a callback instead of a string 
function setInterval(cb, ms) {
	evalStr = "(" + cb.toString() + ")();";
	return app.setInterval(evalStr, ms);
}

var TICK_INTERVAL = 33;

// Globals
var pixel_fields = [];
var field = [];
var previous_field = [];
var interval = 0;
var frame_number = 0;

//INSERT_FRAME_DATA

function video_init() {
	frame_number = 0;

	// Gather references to pixel field objects
	// and initialize game state
	for (var x = 0; x < ###GRID_WIDTH###; ++x) {
		pixel_fields[x] = [];
		field[x] = [];
        previous_field[x] = [];
		for (var y = 0; y < ###GRID_HEIGHT###; ++y) {
			pixel_fields[x][y] = this.getField(`P_${x}_${y}`);
			field[x][y] = 0;
			previous_field[x][y] = 1;
		}
	}

	// Start timer
	interval = setInterval(game_tick, TICK_INTERVAL);

	// Hide start button
	this.getField("B_start").hidden = true;
}

function game_over() {
	app.clearInterval(interval);
	app.alert(`The end, refresh to restart! Follow me @linguinelabs on twitter =)`);
}

const frameField = this.getField("T_frame"); 

function draw_updated_frame_num() {
	frameField.value = `Frame: ${frame_number}`;
}

function set_pixel(x, y, state) {
	pixel_fields[x][###GRID_HEIGHT### - 1 - y].hidden = !state;
}

function draw_field() {
    for (var x = 0; x < ###GRID_WIDTH###; ++x) {
        for (var y = 0; y < ###GRID_HEIGHT###; ++y) {
            if (field[x][y] !== previous_field[x][y]) { // Only update changed pixels
                set_pixel(x, y, field[x][y]);
                previous_field[x][y] = field[x][y]; // Update the previous state
            }
        }
    }
}


function game_tick() {

    // Set the current row to black
    if (frame_number >= 6572) {
	    game_over();
		return;
	}
	const current_frame = frames[frame_number];
	var index = 0
	for (var y = 0; y < ###GRID_HEIGHT###; ++y) {
        for (var x = 0; x < ###GRID_WIDTH###; ++x) {
            field[x][y] = current_frame[index++] == "1" ? 1 : 0;
        }
	}

    // Increment the row counter
    frame_number++;
	draw_updated_frame_num();

    // Update the game state and draw the field
    draw_field();
}

// Zoom to fit (on FF)
app.execMenuItem("FitPage");

endstream
endobj


18 0 obj
<<
  /JS 43 0 R
  /S /JavaScript
>>
endobj


43 0 obj
<< >>
stream



endstream
endobj

trailer
<<
  /Root 1 0 R
>>

%%EOF
"""

PLAYING_FIELD_OBJ = """
###IDX### obj
<<
  /FT /Btn
  /Ff 1
  /MK <<
    /BG [
      0.8
    ]
    /BC [
      0 0 0
    ]
  >>
  /Border [ 0 0 1 ]
  /P 16 0 R
  /Rect [
    ###RECT###
  ]
  /Subtype /Widget
  /T (playing_field)
  /Type /Annot
>>
endobj
"""

PIXEL_OBJ = """
###IDX### obj
<<
  /FT /Btn
  /Ff 1
  /MK <<
    /BG [
      ###COLOR###
    ]
    /BC [
      0.5 0.5 0.5
    ]
  >>
  /Border [ 0 0 1 ]
  /P 16 0 R
  /Rect [
    ###RECT###
  ]
  /Subtype /Widget
  /T (P_###X###_###Y###)
  /Type /Annot
>>
endobj
"""

BUTTON_AP_STREAM = """
###IDX### obj
<<
  /BBox [ 0.0 0.0 ###WIDTH### ###HEIGHT### ]
  /FormType 1
  /Matrix [ 1.0 0.0 0.0 1.0 0.0 0.0]
  /Resources <<
    /Font <<
      /HeBo 10 0 R
    >>
    /ProcSet [ /PDF /Text ]
  >>
  /Subtype /Form
  /Type /XObject
>>
stream
q
0.75 g
0 0 ###WIDTH### ###HEIGHT### re
f
Q
q
1 1 ###WIDTH### ###HEIGHT### re
W
n
BT
/HeBo 12 Tf
0 g
10 8 Td
(###TEXT###) Tj
ET
Q
endstream
endobj
"""

BUTTON_OBJ = """
###IDX### obj
<<
  /A <<
	  /JS ###SCRIPT_IDX### R
	  /S /JavaScript
	>>
  /AP <<
    /N ###AP_IDX### R
  >>
  /F 4
  /FT /Btn
  /Ff 65536
  /MK <<
    /BG [
      0.75
    ]
    /CA (###LABEL###)
  >>
  /P 16 0 R
  /Rect [
    ###RECT###
  ]
  /Subtype /Widget
  /T (###NAME###)
  /Type /Annot
>>
endobj
"""

TEXT_OBJ = """
###IDX### obj
<<
	/AA <<
		/K <<
			/JS ###SCRIPT_IDX### R
			/S /JavaScript
		>>
	>>
	/F 4
	/FT /Tx
	/MK <<
	>>
	/MaxLen 0
	/P 16 0 R
	/Rect [
		###RECT###
	]
	/Subtype /Widget
	/T (###NAME###)
	/V (###LABEL###)
	/Type /Annot
>>
endobj
"""

STREAM_OBJ = """
###IDX### obj
<< >>
stream
###CONTENT###
endstream
endobj
"""

# p1 = PIXEL_OBJ.replace("###IDX###", "50 0").replace("###COLOR###","1 0 0").replace("###RECT###", "460 700 480 720")

PX_SIZE = 12
GRID_WIDTH = 48
GRID_HEIGHT = 36
GRID_OFF_X = 18
GRID_OFF_Y = 300

fields_text = ""
field_indexes = []
obj_idx_ctr = 50

def add_field(field):
	global fields_text, field_indexes, obj_idx_ctr
	fields_text += field
	field_indexes.append(obj_idx_ctr)
	obj_idx_ctr += 1


# Playing field outline
playing_field = PLAYING_FIELD_OBJ
playing_field = playing_field.replace("###IDX###", f"{obj_idx_ctr} 0")
playing_field = playing_field.replace("###RECT###", f"{GRID_OFF_X} {GRID_OFF_Y} {GRID_OFF_X+GRID_WIDTH*PX_SIZE} {GRID_OFF_Y+GRID_HEIGHT*PX_SIZE}")
add_field(playing_field)

for x in range(GRID_WIDTH):
	for y in range(GRID_HEIGHT):
		# Build object
		pixel = PIXEL_OBJ
		pixel = pixel.replace("###IDX###", f"{obj_idx_ctr} 0")
		c = [0, 0, 0]
		pixel = pixel.replace("###COLOR###", f"{c[0]} {c[1]} {c[2]}")
		pixel = pixel.replace("###RECT###", f"{GRID_OFF_X+x*PX_SIZE} {GRID_OFF_Y+y*PX_SIZE} {GRID_OFF_X+x*PX_SIZE+PX_SIZE} {GRID_OFF_Y+y*PX_SIZE+PX_SIZE}")
		pixel = pixel.replace("###X###", f"{x}")
		pixel = pixel.replace("###Y###", f"{y}")

		add_field(pixel)

def add_button(label, name, x, y, width, height, js):
	script = STREAM_OBJ
	script = script.replace("###IDX###", f"{obj_idx_ctr} 0")
	script = script.replace("###CONTENT###", js)
	add_field(script)

	ap_stream = BUTTON_AP_STREAM;
	ap_stream = ap_stream.replace("###IDX###", f"{obj_idx_ctr} 0")
	ap_stream = ap_stream.replace("###TEXT###", label)
	ap_stream = ap_stream.replace("###WIDTH###", f"{width}")
	ap_stream = ap_stream.replace("###HEIGHT###", f"{height}")
	add_field(ap_stream)

	button = BUTTON_OBJ
	button = button.replace("###IDX###", f"{obj_idx_ctr} 0")
	button = button.replace("###SCRIPT_IDX###", f"{obj_idx_ctr-2} 0")
	button = button.replace("###AP_IDX###", f"{obj_idx_ctr-1} 0")
	button = button.replace("###NAME###", name if name else f"B_{obj_idx_ctr}")
	button = button.replace("###RECT###", f"{x} {y} {x + width} {y + height}")
	add_field(button)

def add_text(label, name, x, y, width, height, js):
	script = STREAM_OBJ
	script = script.replace("###IDX###", f"{obj_idx_ctr} 0")
	script = script.replace("###CONTENT###", js)
	add_field(script)

	text = TEXT_OBJ
	text = text.replace("###IDX###", f"{obj_idx_ctr} 0")
	text = text.replace("###SCRIPT_IDX###", f"{obj_idx_ctr-1} 0")
	text = text.replace("###LABEL###", label)
	text = text.replace("###NAME###", name)
	text = text.replace("###RECT###", f"{x} {y} {x + width} {y + height}")
	add_field(text)


add_button("Play", "B_start", GRID_OFF_X + (GRID_WIDTH*PX_SIZE)/2-50, GRID_OFF_Y + (GRID_HEIGHT*PX_SIZE)/2-50, 100, 100, "video_init();")

add_text("Frame: 0", "T_frame", GRID_OFF_X + (GRID_WIDTH * PX_SIZE)/2 - 50, GRID_OFF_Y - 30, 100, 20, "")

filled_pdf = PDF_FILE_TEMPLATE.replace("###FIELDS###", fields_text)
filled_pdf = filled_pdf.replace("###FIELD_LIST###", " ".join([f"{i} 0 R" for i in field_indexes]))
filled_pdf = filled_pdf.replace("###GRID_WIDTH###", f"{GRID_WIDTH}")
filled_pdf = filled_pdf.replace("###GRID_HEIGHT###", f"{GRID_HEIGHT}")


# Practice encoding the video into 01 strings
downsample_side_length = 10
video_path = "badapple.mp4"
cap = cv2.VideoCapture(video_path)
width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
ret, frame = cap.read()

frames = []
while ret:
    encoding = ""
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # row by row
    for y in range(0, height, downsample_side_length):
        for x in range(0, width, downsample_side_length):
            pixel = frame[y, x]
            encoding += "0" if pixel > 128 else "1"
    frames.append(encoding)
    ret, frame = cap.read()

frames_str = " var frames=[\n"
for frame in frames:
    frames_str += f"    \"{frame}\",\n"
frames_str += "];"
filled_pdf = filled_pdf.replace("//INSERT_FRAME_DATA", frames_str)

pdffile = open("out/out.pdf","w")
pdffile.write(filled_pdf)
pdffile.close()