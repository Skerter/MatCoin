#!/bin/bash

if [ ! -d ".venv" ]; then
    echo "Виртуальное окружение не найдено, создаю новое..."
    python3 -m venv .venv
else
    echo "Виртуальное окружение найдено, активирую его..."
fi

. .venv/bin/activate

echo "Устанавливаю зависимости из requirements.txt..."
pip3 install -r requirements.txt

echo "Удаляю старые сборки в bin..."
rm -rf bin

echo "Запускаю сборку с Buildozer..."
buildozer android debug