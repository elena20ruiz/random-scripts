
from xml.etree import ElementTree as et
from xml.etree.ElementTree import tostring
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

from textwrap import wrap


import sys

from utils import log


RATIOS = {
    18: {
        'size': '66px',
        'init': (421,298)
    },
    25: {
        'size': '50px',
        'init': (300, 298)
    },
    'inf': {
        'size': '50px',
        'init': (300, 298)
    }
}

START = {
    1: '298',
    2: '265',
    3: '230',
    4: '200'
}



def run(path, sentences_file):

    # 1. Read file
    log.info('0. Open and read file to get all the text to generate.')
    sentences = read_file(path + '/' + sentences_file) 

    i = 0
    for sentence in sentences:
        log.info(f'1/4 Reading sentence: {sentence}')

        name_file = 'output_' + str(i)
        image = generate(sentence, name_file, path)
        save_file(path, image, name_file)
        i += 1
    return

def generate(sentence, name_file, path):
    
    lsen = len(sentence)
    ratio = get_ratio(lsen)
    lines = wrap(sentence, 18)
    
    log.info(f'2/4 Creating {name_file} file')

    doc = et.Element('svg', width='841.89', height='596.27559', version='1.2', xmlns='http://www.w3.org/2000/svg')
    
    # Append background
    et.SubElement(doc, 'image', href=path + '/background.png', width='841.89', height='596.27559')

    # Create text area an add line
    text = et.Element('text',
                        x='421',
                        y=START[len(lines)],
                        width='841.89', 
                        height='596.27559',
                        fill='#595959',
                        style='font-family:Montserrat;font-size:50px;text-anchor:middle;dominant-baseline:top')
    
    
    
    dy = 0
    for line in lines:
        t = et.Element('tspan',
            x='421',
            dy = str(dy),
            fill='#595959',
            style='font-family:Montserrat;font-size:50px;text-anchor:middle;dominant-baseline:top; font-weight:bold')
        t.text = line
        text.append(
            t
        )
        if dy == 0:
            dy += 70
    doc.append(text)
    return doc

# ------------------------------------
#  Procedures to adapt
#  sentences from their sizes
# ------------------------------------
def get_ratio(s_len):
    if s_len <= 18:
        return RATIOS[18]
    elif s_len <= 25:
        return RATIOS[25]
    else:
        return RATIOS['inf']

# -----------------------------------
#  I/O Procedures
# -----------------------------------

def read_file(path):
    with open(path, "r") as f:
        sentences = f.readlines()
    return sentences

def save_file(path, image, name_file):
    log.info(f'4/4 Saving image: {name_file}')
    with open(name_file + '.svg', 'w') as f:
        f.write('<?xml version=\"1.0\" standalone=\"no\"?>\n')
        f.write('<!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.1//EN\"\n')
        f.write('\"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd\">\n')
        f.write(tostring(image, encoding="unicode"))

    drawing = svg2rlg(name_file + '.svg')
    renderPDF.drawToFile(drawing, name_file + '.pdf')
    return True


if __name__ == '__main__':
    if len(sys.argv) < 3:
        log.error('Bad arguments. Required: Images text file path')
    run(sys.argv[1], sys.argv[2])
