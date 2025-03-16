from Bio import motifs
from Bio.motifs import meme
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
import subprocess
import random


# 1. Генерация случайной последовательности ДНК длиной 10 000 символов
def generate_random_dna_sequence(length):
    return ''.join(random.choices('ACGT', k=length))

# 2. Создание последовательности
dna_sequence = generate_random_dna_sequence(10000)

# 3. Создание объекта SeqRecord
record = SeqRecord(
    Seq(dna_sequence),  # Последовательность ДНК
    id="test_sequence",  # Идентификатор последовательности
    description="Random DNA sequence of length 10000"  # Описание
)

# 4. Запись в файл FASTA
with open("dna_sequence.fasta", "w") as output_file:
    SeqIO.write(record, output_file, "fasta")

print("Файл 'test_sequence.fasta' успешно создан.")

# 1. Загрузка последовательностей из файла FASTA
sequences = []
with open("dna_sequences.fasta", "r") as fasta_file:
    for record in SeqIO.parse(fasta_file, "fasta"):
        sequences.append(record.seq)

# 2. Запись последовательностей во временный файл
with open("temp_sequences.fasta", "w") as temp_file:
    for seq in sequences:
        temp_file.write(f">sequence\n{seq}\n")

# 3. Запуск MEME через командную строку
meme_command = [
    "meme",  # Команда для запуска MEME
    "temp_sequences.fasta",  # Входной файл
    "-o", "meme_output",  # Папка для вывода результатов
    "-dna",  # Тип последовательностей (ДНК)
    "-mod", "zoops",  # Модель поиска (Zero or One Per Sequence)
    "-nmotifs", "3",  # Количество мотивов для поиска
    "-minw", "6",  # Минимальная длина мотива
    "-maxw", "12",  # Максимальная длина мотива
]

# Запуск MEME
subprocess.run(meme_command)

# 4. Чтение результатов MEME
with open("meme_output/meme.txt", "r") as meme_file:
    record = meme.read(meme_file)

# 5. Вывод найденных мотивов
for i, motif in enumerate(record):
    print(f"Мотив {i + 1}:")
    print(motif)
    print("Счетчик нуклеотидов:")
    print(motif.counts)
    print("Логотип мотива:")
    motif.weblogo("motif_logo.png")  # Сохранение логотипа мотива