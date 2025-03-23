DICTOR client:
import speech_recognition as sr
import os
from datetime import datetime

def setup_recognizer():
    """Настройка распознавателя речи"""
    recognizer = sr.Recognizer()
    return recognizer

def setup_microphone(recognizer, source):
    """Настройка микрофона"""
    print("Калибровка микрофона...")
    recognizer.adjust_for_ambient_noise(source, duration=1)
    print("Микрофон готов к использованию.")

def save_to_file(text: str, file_path: str) -> bool:
    """Сохранение текста в файл (без даты)
    
    Args:
        text: Текст для сохранения
        file_path: Путь к файлу
        
    Returns:
        bool: Успешность операции
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:  # 'w' для перезаписи
            f.write(f"{text}\n")  # Сохраняем только текст
        return True
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")
        return False

def main():
    """Основная функция программы"""
    # Настройка путей
    network_path = r"\\msi\users"
    
    # Создание директорий
    for path in [network_path]:
        try:
            os.makedirs(path, exist_ok=True)
            print(f"Директория создана или уже существует: {path}")
        except OSError as e:
            print(f"Ошибка при создании директории {path}: {e}")
    
    # Настройка распознавателя
    recognizer = setup_recognizer()
    
    # Использование микрофона
    with sr.Microphone() as source:
        # Настройка микрофона
        setup_microphone(recognizer, source)
        
        print("Готов к записи. Говорите...")
        while True:
            try:
                # Запись аудио
                audio = recognizer.listen(source, phrase_time_limit=5)
                
                # Распознавание речи
                try:
                    text = recognizer.recognize_google(audio, language='ru-RU')
                    print(f"Вы сказали: {text}")
                    
                    # Сохранение в директорию (перезапись файла)
                    if os.path.exists(network_path):
                        file_path = os.path.join(network_path, "recordings.txt")
                        if save_to_file(text, file_path):
                            print(f"Текст сохранен в {file_path}")
                    else:
                        print(f"Директория недоступна: {network_path}")
                            
                except sr.UnknownValueError:
                    print("Не удалось распознать речь. Попробуйте снова.")
                except sr.RequestError as e:
                    print(f"Ошибка сервиса: {e}")
                    
            except KeyboardInterrupt:
                print("\nЗавершение работы...")
                break
            except Exception as e:
                print(f"Неожиданная ошибка: {e}")
                continue  # Продолжаем работу после ошибки

if __name__ == "__main__":
    main()
