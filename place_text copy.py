import svgwrite
import sys
import base64
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



def run(path, sentences_file):

    # 1. Read file
    log.info('0. Open and read file to get all the text to generate.')
    sentences = read_file(path + '/' + sentences_file) 

    i = 0
    for sentence in sentences:
        log.info(f'1/4 Reading sentence: {sentence}')

        name_file = 'output_' + str(i) + '.svg'
        image = generate(sentence, name_file, path)
        save_file(path, image, name_file)
        i += 1
    return

def generate(sentence, name_file, path):
    
    lsen = len(sentence)
    ratio = get_ratio(lsen)
    new_sent = break_sentence(lsen, sentence)
    
    log.info(f'2/4 Creating {name_file} file')
    drw = svgwrite.Drawing(name_file, profile='tiny')
    
    # Append background
    drw.add(svgwrite.image.Image(path + '/background.png', insert=(0,0), size=(841.89, 596.27559)))

    # Adding text
    drw.add(drw.text(new_sent,
        insert=ratio['init'],
        fill='#595959',
        font_size=ratio['size'],
        font_weight="bold",
        font_family="Montserrat",
        text_anchor="middle")
    )
    return drw

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

def break_sentence(s_len, sentence):
    if s_len <= 18:
        return sentence
    else:
        words = sentence.split(' ')
        final_sentence = ''
        i = 0
        for w in words:
            i += len(w)
            if i + len(w) <= 18:
                i += len(w)
                final_sentence += ' ' + w
            else:
                i = len(w)
                final_sentence += '\n ' + w
    return final_sentence


# -----------------------------------
#  I/O Procedures
# -----------------------------------

def read_file(path):
    with open(path, "r") as f:
        sentences = f.readlines()
    return sentences

def save_file(path, image, name_file):
    log.info(f'4/4 Saving image: {name_file}')
    image.save(path + '/' + name_file)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        log.error('Bad arguments. Required: Images text file path')
    run(sys.argv[1], sys.argv[2])
