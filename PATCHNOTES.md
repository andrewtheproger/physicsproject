# Patch notes for 3800 las project

# 1.5.0
- Добавлена возможность просмотра задач по разделам
- Добавлена возможность прикрепления ответа к задаче
- Исправлен мобильный рендеринг
- Страница "О проекте" стала значительно менее убогой
- Багфиксы

# 1.4.0
- Оптимизировано время загрузки сайта - сейчас упираться начали в потолок хостинга.
- Оптимизирован список задач: всё начало грузиться быстрее. Теперь постраничный лист работает с серверной фильтрацией, а не с клиентской.
- Расширена страница "О проекте": добавлена статистика, лицензия
- Несколько улучшений в дизайне

#### Известные проблемы:
- Иногда нельзя перейти на страницу пользователя: компонент не прогружается движком. Однократный F5 помогает до следующего сброса кэша.

# 1.3.0
- Добавлен красивый редактор LaTeX - Ace. Поддерживается подсветка синтаксиса, нумерация строк, цветовые схемы и прочая красота.
- Добавлена возможность изменять размер шрифта в редакторе LaTeX
- Теперь все цвета на сайте настраиваются со страницы настроек пользователя
- Добавлен выбор цветовых схем из предустановленных
- Минорные изменения интерфейса

# 1.2.0

- Добавлена страница редактирования задачи. Страница доступна только админам
- Добавлена возможность удалять задачи. Действие доступно только админам
- Расширены возможности кастомизации цветовой схемы: добавлена возможность кастомизировать цвет фона и шрифта кнопкок действия
- На странице пользователя отображается дата регистрации
- Теперь ссылки на странице "О проекте" открываются в новой вкладке
- Добавлена кнопка "Скопировать всё" для редактора LaTeX
- Научили редактор LaTeX сохранять промежуточный результат работы, чтобы не терять его при перезагрузке страницы

# 1.1.2
- Добавлен редактор LaTeX.

# 1.1.1

- Добавлена возможность сброса цветовой схемы на стандартную.
- Багфиксы

# 1.1.0

- Добавлена аутентификация на сайте
- API теперь защищено авторизацией
- Добавлены две роли: юзер и админ:
    - Пользователь без роли может только читать данные
    - Юзер может добавлять задачи
    - Админ может редактировать и удалять задачи
- Добавлена пагинация при поиске задач
- Добавлена возможность пользователю настраивать цветовую схему сайта
- Добавлен предикативный поиск задач
- Добавлена валидация ввода пользователя
- Изменены правила ввода номера задачи на UI:

    - Было: номер задачи должен был быть записан только через точку
    - Стало: номер задачи теперь можно записывать через точку, запятую и пробел - он автоматически превратится в номер через точку
- Багфиксы


# 1.0.0

Сделан основной интерфейс:

- Поиск задачи
- Добавление задачи
