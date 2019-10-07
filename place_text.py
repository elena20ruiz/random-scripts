import svgwrite
import sys
import base64
from utils import log


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
    log.info(f'2/4 Creating {name_file} file')
    
    drw = svgwrite.Drawing(name_file, profile='tiny')
    
    # Append background
    drw.add(svgwrite.image.Image(path + '/background.png', insert=(0,0), size=(841.89, 596.27559)))

    # Adding text
    drw.add(drw.text(sentence,
        insert=(50,180),
        fill='#595959',
        font_size='66px',
        font_weight="bold",
        font_family="Courier New")
    )
    return drw

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
