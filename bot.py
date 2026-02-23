<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Прозрачный холст</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        html, body {
            width: 100%;
            height: 100%;
            overflow: auto;
            background: transparent !important;
        }
        
        body {
            font-family: Arial, sans-serif;
            background: transparent !important;
            display: flex;
            flex-direction: column;
            min-height: 1232px; /* 1152 (холст) + 80 (панель) */
        }
        
        /* ПАНЕЛЬ УПРАВЛЕНИЯ - КОМПАКТНАЯ */
        #controls {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 5px 15px;
            display: flex;
            flex-direction: column;
            gap: 5px;
            z-index: 10000;
            width: 100%;
            border-bottom: 2px solid #ffd700;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
            height: 80px; /* Фиксированная высота 80px */
            overflow: hidden;
            flex-shrink: 0;
            justify-content: center;
        }
        
        .controls-row {
            display: flex;
            gap: 8px;
            align-items: center;
            flex-wrap: wrap;
            width: 100%;
            padding: 3px 8px;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 6px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            border-left: 3px solid #ffd700;
        }
        
        #thumbnails-container {
            display: flex;
            align-items: center;
            overflow-x: auto;
            height: 40px;
            background: rgba(255, 255, 255, 0.98);
            border-radius: 6px;
            padding: 2px 8px;
            flex: 1;
            min-width: 200px;
            border: 1px solid #ffd700;
        }
        
        #thumbnails {
            display: flex;
            gap: 8px;
        }
        
        .thumbnail {
            position: relative;
            width: 35px;
            height: 35px;
            flex-shrink: 0;
            border: 2px solid transparent;
            cursor: pointer;
            border-radius: 4px;
            overflow: hidden;
            background: white;
            transition: transform 0.2s;
        }
        
        .thumbnail:hover {
            transform: scale(1.1);
            border-color: #ffd700;
        }
        
        .thumbnail img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        
        .text-thumbnail {
            display: flex;
            align-items: center;
            justify-content: center;
            background: #f0f0f0;
            border-radius: 3px;
            font-size: 10px;
            overflow: hidden;
            text-overflow: ellipsis;
            padding: 0 2px;
            text-align: center;
            width: 100%;
            height: 100%;
            word-break: break-word;
        }
        
        .sound-thumbnail {
            display: flex;
            align-items: center;
            justify-content: center;
            background: #e0f0ff;
            border-radius: 3px;
            font-size: 10px;
            overflow: hidden;
            text-overflow: ellipsis;
            padding: 0 2px;
            text-align: center;
            width: 100%;
            height: 100%;
        }
        
        .widget-thumbnail {
            display: flex;
            align-items: center;
            justify-content: center;
            background: #e8f5e9;
            border-radius: 3px;
            font-size: 10px;
            overflow: hidden;
            text-overflow: ellipsis;
            padding: 0 2px;
            text-align: center;
            width: 100%;
            height: 100%;
            color: #2e7d32;
            font-weight: bold;
        }
        
        .thumbnail.selected {
            border-color: #ffd700;
            box-shadow: 0 0 10px gold;
        }
        
        .thumbnail-hidden {
            opacity: 0.5;
        }
        
        .thumbnail-button {
            position: absolute;
            top: -3px;
            right: -3px;
            width: 16px;
            height: 16px;
            border: 1px solid white;
            border-radius: 50%;
            background: #f44336;
            color: white;
            font-size: 10px;
            line-height: 1;
            cursor: pointer;
            padding: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10;
            font-weight: bold;
        }
        
        .thumbnail-button.show {
            background: #4caf50;
        }
        
        #image-controls, #text-controls, #sound-controls, #widget-controls {
            display: none;
            gap: 8px;
            align-items: center;
            background: rgba(255, 255, 255, 0.98);
            padding: 3px 10px;
            border-radius: 6px;
            border-left: 3px solid #ffd700;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        .panel-title {
            font-weight: bold;
            color: #667eea;
            margin-right: 8px;
            font-size: 12px;
            text-transform: uppercase;
        }
       
        /* КОНТЕЙНЕР ДЛЯ ХОЛСТА */
        #canvas-wrapper {
            width: 100%;
            position: relative;
            overflow: visible;
            background: transparent !important;
            height: 1152px; /* Высота холста 1152px */
            flex-shrink: 0;
        }
        
        .canvas-content {
            position: relative;
            width: 2560px;
            height: 1152px; /* Высота холста 1152px */
            background: transparent !important;
        }
       
        #images-layer, #texts-layer, #widgets-layer {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
        }
        
        #images-layer { z-index: 2; }
        #texts-layer { z-index: 3; }
        #widgets-layer { z-index: 4; }
       
        .draggable-image {
            position: absolute;
            cursor: move;
            user-select: none;
            touch-action: none;
            opacity: 1;
            box-sizing: border-box;
            pointer-events: auto;
            background-color: transparent;
            border: 1px solid rgba(0, 0, 0, 0.1);
            overflow: hidden;
            transform-origin: center center;
        }
        
        .draggable-image img {
            width: 100%;
            height: 100%;
            object-fit: contain;
            pointer-events: none;
            display: block;
        }
        
        .draggable-text {
            position: absolute;
            cursor: move;
            user-select: none;
            touch-action: none;
            box-sizing: content-box;
            opacity: 1;
            display: inline-block;
            white-space: pre-wrap;
            word-wrap: break-word;
            word-break: break-word;
            transform-origin: top left;
            background-color: rgba(255, 255, 255, 0.95);
            padding: 5px 8px;
            border-radius: 3px;
            pointer-events: auto;
            border: 1px solid rgba(0, 0, 0, 0.1);
            min-width: 30px;
            min-height: 30px;
            line-height: 1.3;
            font-size: 14px;
        }
        
        .draggable-widget {
            position: absolute;
            cursor: move;
            user-select: none;
            touch-action: none;
            opacity: 1;
            box-sizing: border-box;
            pointer-events: auto;
            border: 2px solid #4caf50;
            background: white;
            border-radius: 5px;
            overflow: hidden;
            z-index: 4;
        }
        
        .draggable-widget iframe {
            width: 100%;
            height: 100%;
            border: none;
            pointer-events: auto;
        }
        
        .selected {
            position: relative;
            box-shadow: 0 0 0 2px #ffd700 inset;
        }
        
        .locked {
            box-shadow: 0 0 0 2px #ff0000 inset !important;
        }
        
        .resize-handle {
            position: absolute;
            width: 8px;
            height: 8px;
            background-color: #ffd700;
            border: 1px solid #667eea;
            z-index: 10;
            opacity: 0;
            transition: opacity 0.2s;
            cursor: pointer;
            border-radius: 50%;
        }
        
        .rotate-corner {
            position: absolute;
            width: 20px;
            height: 20px;
            background-color: #4caf50;
            border: 2px solid white;
            border-radius: 50%;
            z-index: 10;
            opacity: 0;
            transition: opacity 0.2s;
            cursor: grab;
            top: -25px;
            right: -25px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 12px;
        }
        
        .rotate-corner::after {
            content: "↻";
        }
        
        .resize-n { top: -4px; left: 50%; margin-left: -4px; cursor: n-resize; }
        .resize-ne { top: -4px; right: -4px; cursor: ne-resize; }
        .resize-e { top: 50%; right: -4px; margin-top: -4px; cursor: e-resize; }
        .resize-se { bottom: -4px; right: -4px; cursor: se-resize; }
        .resize-s { bottom: -4px; left: 50%; margin-left: -4px; cursor: s-resize; }
        .resize-sw { bottom: -4px; left: -4px; cursor: sw-resize; }
        .resize-w { top: 50%; left: -4px; margin-top: -4px; cursor: w-resize; }
        .resize-nw { top: -4px; left: -4px; cursor: nw-resize; }
        
        .selected:not(.locked) .resize-handle,
        .selected:not(.locked) .rotate-corner {
            opacity: 1;
        }
        
        button {
            padding: 4px 8px;
            border: none;
            border-radius: 4px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-size: 11px;
            font-weight: bold;
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.2s;
            box-shadow: 0 1px 3px rgba(0,0,0,0.2);
            border: 1px solid rgba(255,255,255,0.3);
        }
        
        button:hover {
            opacity: 0.95;
            transform: translateY(-1px);
            box-shadow: 0 3px 8px rgba(0,0,0,0.2);
        }
        
        button:active {
            transform: translateY(0);
        }
        
        #file-input, #sound-input {
            display: none;
        }
        
        #status {
            margin-left: auto;
            font-size: 11px;
            color: #4caf50;
            white-space: nowrap;
            font-weight: bold;
            background: rgba(255,255,255,0.9);
            padding: 3px 8px;
            border-radius: 10px;
            border: 1px solid #ffd700;
        }
        
        .properties-panel {
            position: fixed;
            top: 100px;
            right: 10px;
            background: rgba(255, 255, 255, 0.98);
            padding: 12px;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            z-index: 2000;
            display: none;
            min-width: 200px;
            backdrop-filter: blur(5px);
            border: 2px solid #ffd700;
        }
        
        #simple-text-input {
            position: fixed;
            z-index: 2000;
            background: rgba(255, 255, 255, 0.98);
            border: 2px solid #ffd700;
            border-radius: 8px;
            padding: 0;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            display: none;
            min-width: 350px;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            backdrop-filter: blur(5px);
        }
        
        #simple-text-input textarea {
            width: 100%;
            min-height: 100px;
            padding: 10px;
            border: none;
            border-radius: 8px 8px 0 0;
            resize: both;
            font-family: Arial, sans-serif;
            font-size: 14px;
            box-sizing: border-box;
            outline: none;
        }
        
        .text-toolbar {
            display: flex;
            gap: 8px;
            padding: 10px;
            background: rgba(245, 245, 245, 0.95);
            border-top: 1px solid #ffd700;
            flex-wrap: wrap;
            border-radius: 0 0 8px 8px;
        }
        
        .sound-visualization {
            width: 100px;
            height: 25px;
            background: #ddd;
            border-radius: 12px;
            overflow: hidden;
            position: relative;
            border: 1px solid #667eea;
        }
        
        .sound-progress {
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            width: 0%;
            transition: width 0.1s;
        }
        
        #audio-element {
            display: none;
        }
        
        .volume-control {
            display: flex;
            align-items: center;
            gap: 5px;
        }
        
        .volume-slider {
            width: 60px;
        }
        
        #tts-panel, #widgets-panel, #crop-panel {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(255, 255, 255, 0.98);
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 8px 30px rgba(0,0,0,0.4);
            z-index: 2000;
            display: none;
            width: 400px;
            max-width: 90vw;
            max-height: 80vh;
            overflow-y: auto;
            backdrop-filter: blur(5px);
            border: 2px solid #ffd700;
        }
        
        .rotate-indicator {
            position: absolute;
            top: -20px;
            left: 50%;
            transform: translateX(-50%);
            font-size: 10px;
            color: #ffd700;
            background: #667eea;
            padding: 2px 6px;
            border-radius: 10px;
            display: none;
            font-weight: bold;
            border: 1px solid white;
        }
        
        .selected .rotate-indicator {
            display: block;
        }
        
        .crop-btn {
            background: linear-gradient(135deg, #ff9800, #f44336) !important;
        }
        
        .panel-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        
        .panel-header h3 {
            margin: 0;
            color: #333;
            font-size: 16px;
        }
        
        .close-btn {
            background: #f44336;
            color: white;
            border: none;
            border-radius: 50%;
            width: 25px;
            height: 25px;
            cursor: pointer;
            font-size: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .crop-preview {
            width: 100%;
            height: 150px;
            border: 1px solid #ffd700;
            margin-bottom: 10px;
            overflow: hidden;
            position: relative;
            background: #f5f5f5;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 5px;
        }
        
        .crop-controls {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
            margin-bottom: 10px;
        }
        
        .crop-control {
            display: flex;
            flex-direction: column;
        }
        
        .crop-control label {
            font-size: 11px;
            margin-bottom: 3px;
            color: #666;
            font-weight: bold;
        }
        
        .crop-control input {
            padding: 5px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 11px;
        }
        
        .crop-buttons {
            display: flex;
            gap: 8px;
        }
        
        .crop-buttons button {
            flex: 1;
        }
        
        #apply-crop-btn {
            background: linear-gradient(135deg, #4caf50, #45a049);
        }
        
        #cancel-crop-btn {
            background: linear-gradient(135deg, #f44336, #d32f2f);
        }
        
        .widgets-tabs {
            display: flex;
            gap: 5px;
            margin-bottom: 10px;
            border-bottom: 1px solid #ffd700;
            padding-bottom: 5px;
        }
        
        .widgets-tab {
            padding: 5px 10px;
            background: #f5f5f5;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 11px;
            font-weight: bold;
        }
        
        .widgets-tab.active {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
        }
        
        .widgets-content {
            display: none;
        }
        
        .widgets-content.active {
            display: block;
        }
        
        .widget-url-input,
        .widget-name-input {
            width: 100%;
            padding: 8px;
            margin-bottom: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
            font-size: 11px;
        }
        
        .widget-size-controls {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
            margin-bottom: 8px;
        }
        
        .widget-button {
            width: 100%;
            padding: 8px;
            margin-bottom: 5px;
            background: linear-gradient(135deg, #4caf50, #45a049);
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 11px;
            font-weight: bold;
        }
        
        .saved-widgets-list {
            margin-top: 10px;
            max-height: 150px;
            overflow-y: auto;
        }
        
        .saved-widget-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 5px;
            background: #f9f9f9;
            border-radius: 4px;
            margin-bottom: 3px;
            border: 1px solid #ffd700;
        }
        
        .saved-widget-name {
            flex-grow: 1;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            font-weight: bold;
            font-size: 11px;
        }
        
        .widget-actions {
            display: flex;
            gap: 3px;
        }
        
        .add-widget-btn {
            background: #4caf50;
            color: white;
        }
        
        .remove-widget-btn {
            background: #f44336;
            color: white;
        }

        /* Полосы прокрутки */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(255,255,255,0.3);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 4px;
            border: 1px solid #ffd700;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #764ba2, #667eea);
        }
    </style>
</head>
<body>
    <div id="controls">
        <!-- Первая строка - основные кнопки -->
        <div class="controls-row" style="background: linear-gradient(135deg, #e3f2fd, #bbdefb);">
            <span style="font-weight: bold; color: #1976d2; font-size: 12px;">📋 Инструменты:</span>
            <button onclick="document.getElementById('file-input').click()">🖼 Изображение</button>
            <button id="add-text-btn">📝 Текст</button>
            <button id="add-sound-btn">🔊 Звук</button>
            <button id="add-widget-btn">🧩 Виджет</button>
            <button id="speak-text-btn">🗣 Озвучить</button>
            <button id="clear-btn">🗑 Очистить</button>
            <div id="status">✅ Синхронизировано</div>
        </div>
        
        <!-- Вторая строка - миниатюры -->
        <div class="controls-row">
            <span style="font-weight: bold; color: #1976d2; font-size: 12px;">🖼 Элементы:</span>
            <div id="thumbnails-container">
                <div id="thumbnails"></div>
            </div>
        </div>
        
        <!-- Третья строка - панель изображений -->
        <div id="image-controls" class="controls-row">
            <span class="panel-title">🖼 Изображение:</span>
            <button id="hide-btn">👁 Скрыть</button>
            <button id="delete-btn">🗑 Удалить</button>
            <button id="settings-btn">⚙ Настройки</button>
            <button id="lock-btn">🔒 Закрепить</button>
            <button id="flip-h-btn">↔ Гориз</button>
            <button id="flip-v-btn">↕ Вертик</button>
            <button id="crop-image-btn" class="crop-btn">✂ Обрезать</button>
        </div>
        
        <!-- Четвертая строка - панель текста -->
        <div id="text-controls" class="controls-row">
            <span class="panel-title">📝 Текст:</span>
            <button id="hide-text-btn">👁 Скрыть</button>
            <button id="edit-text-btn">✏ Редактировать</button>
            <button id="delete-text-btn">🗑 Удалить</button>
            <button id="lock-text-btn">🔒 Закрепить</button>
            <button id="crop-text-btn" class="crop-btn">✂ Обрезать</button>
        </div>
        
        <!-- Пятая строка - панель звука -->
        <div id="sound-controls" class="controls-row">
            <span class="panel-title">🔊 Звук:</span>
            <button id="play-btn">▶</button>
            <button id="pause-btn">⏸</button>
            <div class="sound-visualization">
                <div class="sound-progress" id="sound-progress"></div>
            </div>
            <div class="volume-control">
                <span>🔊</span>
                <input type="range" class="volume-slider" id="volume-slider" min="0" max="100" value="100">
            </div>
            <button id="delete-sound-btn">🗑 Удалить</button>
        </div>
        
        <!-- Шестая строка - панель виджетов -->
        <div id="widget-controls" class="controls-row">
            <span class="panel-title">🧩 Виджет:</span>
            <button id="hide-widget-btn">👁 Скрыть</button>
            <button id="delete-widget-btn">🗑 Удалить</button>
            <button id="lock-widget-btn">🔒 Закрепить</button>
            <button id="reload-widget-btn">🔄 Обновить</button>
            <button id="crop-widget-btn" class="crop-btn">✂ Обрезать</button>
        </div>
    </div>
   
    <div id="canvas-wrapper">
        <div class="canvas-content">
            <div id="images-layer"></div>
            <div id="texts-layer"></div>
            <div id="widgets-layer"></div>
        </div>
    </div>
    
    <!-- Панель добавления текста -->
    <div id="simple-text-input">
        <textarea id="text-input-area" placeholder="Введите текст..."></textarea>
        <div class="text-toolbar">
            <select id="font-family-select">
                <option value="'Comic Sans MS', cursive">Comic Sans</option>
                <option value="Arial, sans-serif">Arial</option>
                <option value="'Times New Roman', serif">Times New Roman</option>
                <option value="Verdana, sans-serif">Verdana</option>
            </select>
            <input type="range" id="font-size-slider" min="12" max="72" value="16">
            <input type="color" id="text-color-picker" value="#000000">
            <button id="apply-text-simple">✅ Готово</button>
            <button id="cancel-text-simple" style="background: #f44336;">❌ Отмена</button>
        </div>
    </div>
   
    <!-- Панель свойств изображения -->
    <div class="properties-panel" id="properties-panel">
        <div class="panel-header">
            <h3>⚙ Свойства</h3>
            <button class="close-btn" id="close-properties">×</button>
        </div>
        <label>
            Прозрачность:
            <input type="range" id="opacity-slider" min="0" max="100" value="100">
        </label>
        <label>
            Яркость:
            <input type="range" id="brightness-slider" min="0" max="200" value="100">
        </label>
    </div>
   
    <!-- Панель TTS -->
    <div id="tts-panel">
        <div class="panel-header">
            <h3>🗣 Озвучивание</h3>
            <button class="close-btn" id="tts-close-btn">×</button>
        </div>
        <textarea id="tts-text-input" placeholder="Введите текст для озвучивания..."></textarea>
       
        <div class="tts-controls-row">
            <select id="tts-voice-select" style="flex: 1; padding: 5px; font-size: 11px;">
                <option value="">Выберите голос...</option>
            </select>
        </div>
       
        <div class="tts-controls-row" style="display: flex; align-items: center; gap: 5px; margin: 5px 0;">
            <span style="font-size: 11px;">Скорость:</span>
            <input type="range" id="tts-rate-slider" min="0.5" max="2" step="0.1" value="1" style="flex: 1;">
            <span id="tts-rate-value" style="font-size: 11px;">1.0</span>
        </div>
        
        <div class="tts-controls-row" style="display: flex; align-items: center; gap: 5px; margin: 5px 0;">
            <span style="font-size: 11px;">Высота:</span>
            <input type="range" id="tts-pitch-slider" min="0.5" max="2" step="0.1" value="1" style="flex: 1;">
            <span id="tts-pitch-value" style="font-size: 11px;">1.0</span>
        </div>
        
        <div class="tts-controls-row" style="display: flex; align-items: center; gap: 5px; margin: 5px 0;">
            <span style="font-size: 11px;">Громкость:</span>
            <input type="range" id="tts-volume-slider" min="0" max="1" step="0.1" value="1" style="flex: 1;">
            <span id="tts-volume-value" style="font-size: 11px;">1.0</span>
        </div>
       
        <div class="crop-buttons" style="margin-top: 8px;">
            <button id="tts-play-btn" style="background: #4caf50;">▶</button>
            <button id="tts-pause-btn" style="background: #ff9800;">⏸</button>
            <button id="tts-stop-btn" style="background: #f44336;">■</button>
        </div>
    </div>
   
    <!-- Панель виджетов -->
    <div id="widgets-panel">
        <div class="panel-header">
            <h3>🧩 Виджеты</h3>
            <button class="close-btn" id="close-widgets-btn">×</button>
        </div>
        
        <div class="widgets-tabs">
            <button class="widgets-tab active" data-tab="add-widget">➕ Добавить</button>
            <button class="widgets-tab" data-tab="saved-widgets">📦 Сохраненные</button>
        </div>
        
        <div id="add-widget-content" class="widgets-content active">
            <input type="url" class="widget-url-input" id="widget-url-input" 
                   placeholder="URL виджета">
            
            <div class="widget-size-controls">
                <div>
                    <label style="font-size: 11px;">Ширина</label>
                    <input type="number" id="widget-width-input" value="400" min="100" style="font-size: 11px;">
                </div>
                <div>
                    <label style="font-size: 11px;">Высота</label>
                    <input type="number" id="widget-height-input" value="300" min="100" style="font-size: 11px;">
                </div>
            </div>
            
            <input type="text" class="widget-name-input" id="widget-name-input" 
                   placeholder="Название">
            
            <button class="widget-button" id="save-widget-btn">💾 Сохранить</button>
            <button class="widget-button" id="add-widget-direct-btn" style="background: #4285f4;">📌 Добавить</button>
        </div>
        
        <div id="saved-widgets-content" class="widgets-content">
            <div class="saved-widgets-list" id="saved-widgets-list"></div>
        </div>
    </div>

    <!-- Панель обрезки -->
    <div id="crop-panel">
        <div class="panel-header">
            <h3>✂ Обрезка</h3>
            <button class="close-btn" id="close-crop-btn">×</button>
        </div>
        
        <div class="crop-preview" id="crop-preview"></div>
        
        <div class="crop-controls">
            <div>
                <label style="font-size: 11px;">X</label>
                <input type="number" id="crop-x" value="0" min="0" style="font-size: 11px;">
            </div>
            <div>
                <label style="font-size: 11px;">Y</label>
                <input type="number" id="crop-y" value="0" min="0" style="font-size: 11px;">
            </div>
            <div>
                <label style="font-size: 11px;">Ширина</label>
                <input type="number" id="crop-width" value="100" min="10" style="font-size: 11px;">
            </div>
            <div>
                <label style="font-size: 11px;">Высота</label>
                <input type="number" id="crop-height" value="100" min="10" style="font-size: 11px;">
            </div>
        </div>
        
        <div class="crop-buttons">
            <button id="apply-crop-btn">✅ Применить</button>
            <button id="cancel-crop-btn">❌ Отмена</button>
        </div>
    </div>
   
    <input type="file" id="file-input" accept="image/*">
    <input type="file" id="sound-input" accept="audio/*">
    <audio id="audio-element"></audio>
    
    <script src="https://www.gstatic.com/firebasejs/9.6.0/firebase-app-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/9.6.0/firebase-database-compat.js"></script>
   
    <script>
        // Firebase конфигурация
        const firebaseConfig = {
            apiKey: "AIzaSyDNWDm3Rkvq4mV7Cvf5ckvZvDD5MNLDXoo",
            authDomain: "greenbackgroundapp.firebaseapp.com",
            databaseURL: "https://greenbackgroundapp-default-rtdb.europe-west1.firebasedatabase.app",
            projectId: "greenbackgroundapp",
            storageBucket: "greenbackgroundapp.appspot.com",
            messagingSenderId: "857271333291",
            appId: "1:857271333291:web:e754824268f37341c7e2ee"
        };
        
        try {
            firebase.initializeApp(firebaseConfig);
        } catch (error) {
            console.log("Firebase уже инициализирован");
        }
       
        const database = firebase.database();
        const imagesRef = database.ref('images');
        const textsRef = database.ref('texts');
        const soundsRef = database.ref('sounds');
        const widgetsRef = database.ref('widgets');
        const savedWidgetsRef = database.ref('savedWidgets');
       
        // Состояние приложения
        let images = {};
        let texts = {};
        let sounds = {};
        let widgets = {};
        let savedWidgets = {};
        let activeInteraction = null;
        let activeElement = null;
        let startX = 0, startY = 0;
        let startWidth = 0, startHeight = 0;
        let startLeft = 0, startTop = 0;
        let startRotation = 0;
        let selectedImageId = null;
        let selectedTextId = null;
        let selectedSoundId = null;
        let selectedWidgetId = null;
        let actionHistory = [];
        let historyPointer = -1;
        let resizeDirection = null;
        let isAddingText = false;
        let isAddingWidget = false;
        let soundInterval = null;
       
        // Переменные для обрезки
        let cropMode = false;
        let cropElement = null;
        let cropType = null;
       
        // TTS
        let speechSynthesis = window.speechSynthesis;
        let speechUtterance = null;
        let voices = [];
        let isTTSInitialized = false;
        
        // Режим OBS - УДАЛЕН
        
        function initApp() {
            console.log("Инициализация приложения...");
            
            // Показываем все панели для отладки
            document.getElementById('image-controls').style.display = 'flex';
            document.getElementById('text-controls').style.display = 'flex';
            document.getElementById('sound-controls').style.display = 'flex';
            document.getElementById('widget-controls').style.display = 'flex';
            
            // Скрываем их через секунду
            setTimeout(() => {
                if (!selectedImageId) document.getElementById('image-controls').style.display = 'none';
                if (!selectedTextId) document.getElementById('text-controls').style.display = 'none';
                if (!selectedSoundId) document.getElementById('sound-controls').style.display = 'none';
                if (!selectedWidgetId) document.getElementById('widget-controls').style.display = 'none';
            }, 1000);
           
            // Инициализация обработчиков событий
            initEventListeners();
           
            // Подписка на изменения в Firebase
            subscribeToFirebase();
           
            console.log("Приложение инициализировано");
        }
        
        function initEventListeners() {
            // Основные кнопки
            document.getElementById('file-input').addEventListener('change', handleFileUpload);
            document.getElementById('sound-input').addEventListener('change', handleSoundUpload);
            document.getElementById('clear-btn').addEventListener('click', clearCanvas);
            document.getElementById('add-text-btn').addEventListener('click', showSimpleTextInput);
            document.getElementById('apply-text-simple').addEventListener('click', createTextFromSimpleInput);
            document.getElementById('cancel-text-simple').addEventListener('click', cancelSimpleTextInput);
            document.getElementById('speak-text-btn').addEventListener('click', showTTSPanel);
            document.getElementById('add-sound-btn').addEventListener('click', () => {
                document.getElementById('sound-input').click();
            });
            
            // Кнопки изображений
            document.getElementById('hide-btn').addEventListener('click', toggleImageVisibility);
            document.getElementById('delete-btn').addEventListener('click', deleteSelectedImage);
            document.getElementById('settings-btn').addEventListener('click', showImageProperties);
            document.getElementById('lock-btn').addEventListener('click', toggleImageLock);
            document.getElementById('flip-h-btn').addEventListener('click', () => flipImage('horizontal'));
            document.getElementById('flip-v-btn').addEventListener('click', () => flipImage('vertical'));
            document.getElementById('crop-image-btn').addEventListener('click', () => startCrop('image'));
            
            // Кнопки текста
            document.getElementById('hide-text-btn').addEventListener('click', toggleTextVisibility);
            document.getElementById('edit-text-btn').addEventListener('click', editSelectedText);
            document.getElementById('delete-text-btn').addEventListener('click', deleteSelectedText);
            document.getElementById('lock-text-btn').addEventListener('click', toggleTextLock);
            document.getElementById('crop-text-btn').addEventListener('click', () => startCrop('text'));
            
            // Кнопки звука
            document.getElementById('play-btn').addEventListener('click', playSound);
            document.getElementById('pause-btn').addEventListener('click', pauseSound);
            document.getElementById('delete-sound-btn').addEventListener('click', deleteSound);
            document.getElementById('volume-slider').addEventListener('input', updateVolume);
            
            // Кнопки виджетов
            document.getElementById('add-widget-btn').addEventListener('click', showWidgetsPanel);
            document.getElementById('close-widgets-btn').addEventListener('click', closeWidgetsPanel);
            document.getElementById('save-widget-btn').addEventListener('click', saveWidgetFromInput);
            document.getElementById('add-widget-direct-btn').addEventListener('click', addWidgetDirectly);
            document.getElementById('hide-widget-btn').addEventListener('click', toggleWidgetVisibility);
            document.getElementById('delete-widget-btn').addEventListener('click', deleteSelectedWidget);
            document.getElementById('lock-widget-btn').addEventListener('click', toggleWidgetLock);
            document.getElementById('reload-widget-btn').addEventListener('click', reloadSelectedWidget);
            document.getElementById('crop-widget-btn').addEventListener('click', () => startCrop('widget'));
            
            // Вкладки виджетов
            document.querySelectorAll('.widgets-tab').forEach(tab => {
                tab.addEventListener('click', function() {
                    document.querySelectorAll('.widgets-tab').forEach(t => t.classList.remove('active'));
                    document.querySelectorAll('.widgets-content').forEach(c => c.classList.remove('active'));
                    this.classList.add('active');
                    document.getElementById(this.dataset.tab + '-content').classList.add('active');
                });
            });
            
            // Панель свойств
            document.getElementById('close-properties').addEventListener('click', () => {
                document.getElementById('properties-panel').style.display = 'none';
            });
            
            document.getElementById('opacity-slider').addEventListener('input', (e) => {
                if (selectedImageId) {
                    const opacity = e.target.value / 100;
                    const imgElement = document.getElementById(selectedImageId);
                    if (imgElement) imgElement.style.opacity = opacity;
                    imagesRef.child(selectedImageId).update({ opacity });
                }
            });
            
            document.getElementById('brightness-slider').addEventListener('input', (e) => {
                if (selectedImageId) {
                    const brightness = e.target.value;
                    const imgElement = document.getElementById(selectedImageId);
                    if (imgElement) imgElement.style.filter = `brightness(${brightness}%)`;
                    imagesRef.child(selectedImageId).update({ brightness });
                }
            });
            
            // Панель обрезки
            document.getElementById('close-crop-btn').addEventListener('click', cancelCrop);
            document.getElementById('apply-crop-btn').addEventListener('click', applyCrop);
            document.getElementById('cancel-crop-btn').addEventListener('click', cancelCrop);
            
            // TTS
            document.getElementById('tts-close-btn').addEventListener('click', closeTTSPanel);
            document.getElementById('tts-play-btn').addEventListener('click', playTTS);
            document.getElementById('tts-pause-btn').addEventListener('click', pauseTTS);
            document.getElementById('tts-stop-btn').addEventListener('click', stopTTS);
            
            document.getElementById('tts-rate-slider').addEventListener('input', function() {
                document.getElementById('tts-rate-value').textContent = this.value;
            });
            
            document.getElementById('tts-pitch-slider').addEventListener('input', function() {
                document.getElementById('tts-pitch-value').textContent = this.value;
            });
            
            document.getElementById('tts-volume-slider').addEventListener('input', function() {
                document.getElementById('tts-volume-value').textContent = this.value;
            });
            
            // Текстовый редактор
            document.getElementById('font-size-slider').addEventListener('input', updateTextPreview);
            document.getElementById('text-color-picker').addEventListener('input', updateTextPreview);
            document.getElementById('font-family-select').addEventListener('change', updateTextPreview);
            document.getElementById('text-input-area').addEventListener('input', updateTextPreview);
            
            // Клик по пустой области
            document.getElementById('images-layer').addEventListener('mousedown', (e) => {
                if (e.target === document.getElementById('images-layer')) deselectAll();
            });
            document.getElementById('texts-layer').addEventListener('mousedown', (e) => {
                if (e.target === document.getElementById('texts-layer')) deselectAll();
            });
            document.getElementById('widgets-layer').addEventListener('mousedown', (e) => {
                if (e.target === document.getElementById('widgets-layer')) deselectAll();
            });
            
            // Глобальные события
            document.addEventListener('mousemove', handleMove);
            document.addEventListener('touchmove', handleMove, { passive: false });
            document.addEventListener('mouseup', endInteraction);
            document.addEventListener('touchend', endInteraction);
            
            document.addEventListener('keydown', (e) => {
                if (e.ctrlKey && e.key === 'z') {
                    e.preventDefault();
                    undoAction();
                }
                if (e.key === 'Escape') {
                    if (isAddingText) cancelSimpleTextInput();
                    if (isAddingWidget) closeWidgetsPanel();
                    if (cropMode) cancelCrop();
                }
                if (e.key === 'Enter' && e.ctrlKey && isAddingText) {
                    createTextFromSimpleInput();
                }
            });
        }
        
        function subscribeToFirebase() {
            imagesRef.on('value', (snapshot) => {
                images = snapshot.val() || {};
                updateCanvas();
                updateThumbnails();
            });
           
            textsRef.on('value', (snapshot) => {
                texts = snapshot.val() || {};
                updateTexts();
                updateThumbnails();
            });
           
            soundsRef.on('value', (snapshot) => {
                sounds = snapshot.val() || {};
                updateThumbnails();
                if (selectedSoundId && sounds[selectedSoundId]) {
                    updateSoundControls(sounds[selectedSoundId]);
                } else if (selectedSoundId) {
                    selectedSoundId = null;
                    document.getElementById('sound-controls').style.display = 'none';
                }
            });
            
            widgetsRef.on('value', (snapshot) => {
                widgets = snapshot.val() || {};
                updateWidgets();
                updateThumbnails();
            });
            
            savedWidgetsRef.on('value', (snapshot) => {
                savedWidgets = snapshot.val() || {};
                updateSavedWidgetsList();
            });
        }
        
        function updateCanvas() {
            const container = document.getElementById('images-layer');
            
            // Удаляем удаленные изображения
            document.querySelectorAll('.draggable-image').forEach(img => {
                if (!images[img.id]) {
                    img.remove();
                    if (selectedImageId === img.id) selectedImageId = null;
                }
            });
            
            // Обновляем существующие и создаем новые
            for (const id in images) {
                const data = images[id];
                let img = document.getElementById(id);
                
                if (!img) {
                    img = createImageElement(data);
                    container.appendChild(img);
                }
                
                updateImageElement(img, data);
                
                if (data.isNew) {
                    selectImage(id);
                    imagesRef.child(id).update({ isNew: null });
                }
            }
        }
        
        function updateTexts() {
            const container = document.getElementById('texts-layer');
            
            document.querySelectorAll('.draggable-text').forEach(el => {
                if (!texts[el.id]) {
                    el.remove();
                    if (selectedTextId === el.id) selectedTextId = null;
                }
            });
            
            for (const id in texts) {
                const data = texts[id];
                let el = document.getElementById(id);
                
                if (!el) {
                    el = createTextElement(data);
                    container.appendChild(el);
                }
                
                updateTextElement(el, data);
                
                if (data.isNew) {
                    selectText(id);
                    textsRef.child(id).update({ isNew: null });
                }
            }
        }
        
        function updateWidgets() {
            const container = document.getElementById('widgets-layer');
            
            document.querySelectorAll('.draggable-widget').forEach(el => {
                if (!widgets[el.id]) {
                    el.remove();
                    if (selectedWidgetId === el.id) selectedWidgetId = null;
                }
            });
            
            for (const id in widgets) {
                const data = widgets[id];
                let el = document.getElementById(id);
                
                if (!el) {
                    el = createWidgetElement(data);
                    container.appendChild(el);
                }
                
                updateWidgetElement(el, data);
                
                if (data.isNew) {
                    selectWidget(id);
                    widgetsRef.child(id).update({ isNew: null });
                }
            }
        }
        
        function selectImage(id) {
            deselectAll();
            selectedImageId = id;
            const el = document.getElementById(id);
            if (el) {
                el.classList.add('selected');
                document.getElementById('image-controls').style.display = 'flex';
                document.getElementById('lock-btn').textContent = el.classList.contains('locked') ? '🔓 Открепить' : '🔒 Закрепить';
            }
        }
        
        function selectText(id) {
            deselectAll();
            selectedTextId = id;
            const el = document.getElementById(id);
            if (el) {
                el.classList.add('selected');
                document.getElementById('text-controls').style.display = 'flex';
                document.getElementById('lock-text-btn').textContent = el.classList.contains('locked') ? '🔓 Открепить' : '🔒 Закрепить';
            }
        }
        
        function selectSound(id) {
            deselectAll();
            selectedSoundId = id;
            document.getElementById('sound-controls').style.display = 'flex';
            updateSoundControls(sounds[id]);
        }
        
        function selectWidget(id) {
            deselectAll();
            selectedWidgetId = id;
            const el = document.getElementById(id);
            if (el) {
                el.classList.add('selected');
                document.getElementById('widget-controls').style.display = 'flex';
                document.getElementById('lock-widget-btn').textContent = el.classList.contains('locked') ? '🔓 Открепить' : '🔒 Закрепить';
            }
        }
        
        function deselectAll() {
            document.querySelectorAll('.draggable-image, .draggable-text, .draggable-widget').forEach(el => {
                el.classList.remove('selected');
            });
            
            document.getElementById('image-controls').style.display = 'none';
            document.getElementById('text-controls').style.display = 'none';
            document.getElementById('sound-controls').style.display = 'none';
            document.getElementById('widget-controls').style.display = 'none';
            document.getElementById('properties-panel').style.display = 'none';
            
            selectedImageId = null;
            selectedTextId = null;
            selectedSoundId = null;
            selectedWidgetId = null;
        }
        
        function createImageElement(data) {
            const el = document.createElement('div');
            el.id = data.id;
            el.className = 'draggable-image';
            
            const img = document.createElement('img');
            img.src = data.src;
            el.appendChild(img);
            
            addResizeHandles(el);
            addRotateHandle(el);
            
            el.addEventListener('mousedown', startImageDrag);
            el.addEventListener('touchstart', startImageDrag, { passive: false });
            
            return el;
        }
        
        function updateImageElement(el, data) {
            el.style.left = data.x + 'px';
            el.style.top = data.y + 'px';
            el.style.width = data.width + 'px';
            el.style.height = data.height + 'px';
            el.style.opacity = data.opacity || 1;
            el.style.filter = `brightness(${data.brightness || 100}%)`;
            el.style.display = data.display === 'none' ? 'none' : 'block';
            
            if (data.rotation) el.dataset.rotation = data.rotation;
            if (data.flipHorizontal) el.dataset.flipH = 'true';
            if (data.flipVertical) el.dataset.flipV = 'true';
            
            applyTransformations(el);
            
            if (data.locked) {
                el.classList.add('locked');
            } else {
                el.classList.remove('locked');
            }
            
            if (data.crop) {
                el.style.clipPath = `inset(${data.crop.y}px ${data.width - data.crop.x - data.crop.width}px ${data.height - data.crop.y - data.crop.height}px ${data.crop.x}px)`;
            }
        }
        
        function createTextElement(data) {
            const el = document.createElement('div');
            el.id = data.id;
            el.className = 'draggable-text';
            
            addResizeHandles(el);
            
            el.addEventListener('mousedown', startTextDrag);
            el.addEventListener('touchstart', startTextDrag, { passive: false });
            el.addEventListener('dblclick', editSelectedText);
            
            return el;
        }
        
        function updateTextElement(el, data) {
            el.textContent = data.text || '';
            el.style.left = data.x + 'px';
            el.style.top = data.y + 'px';
            el.style.fontSize = (data.fontSize || 16) + 'px';
            el.style.color = data.color || '#000000';
            el.style.fontFamily = data.fontFamily || "'Comic Sans MS', cursive";
            el.style.opacity = data.opacity || 1;
            el.style.display = data.display === 'none' ? 'none' : 'block';
            
            if (data.locked) {
                el.classList.add('locked');
            } else {
                el.classList.remove('locked');
            }
            
            if (data.crop) {
                el.style.overflow = 'hidden';
                el.style.maxWidth = data.crop.width + 'px';
                el.style.maxHeight = data.crop.height + 'px';
            }
        }
        
        function createWidgetElement(data) {
            const el = document.createElement('div');
            el.id = data.id;
            el.className = 'draggable-widget';
            
            const iframe = document.createElement('iframe');
            iframe.src = data.url;
            iframe.style.width = '100%';
            iframe.style.height = '100%';
            iframe.style.border = 'none';
            el.appendChild(iframe);
            
            addResizeHandles(el);
            
            el.addEventListener('mousedown', startWidgetDrag);
            el.addEventListener('touchstart', startWidgetDrag, { passive: false });
            
            return el;
        }
        
        function updateWidgetElement(el, data) {
            el.style.left = data.x + 'px';
            el.style.top = data.y + 'px';
            el.style.width = data.width + 'px';
            el.style.height = data.height + 'px';
            el.style.opacity = data.opacity || 1;
            el.style.display = data.display === 'none' ? 'none' : 'block';
            el.title = data.name || 'Виджет';
            
            if (data.locked) {
                el.classList.add('locked');
            } else {
                el.classList.remove('locked');
            }
            
            const iframe = el.querySelector('iframe');
            if (iframe && iframe.src !== data.url) {
                iframe.src = data.url;
            }
            
            if (data.crop) {
                el.style.clipPath = `inset(${data.crop.y}px ${data.width - data.crop.x - data.crop.width}px ${data.height - data.crop.y - data.crop.height}px ${data.crop.x}px)`;
            }
        }
        
        function addResizeHandles(el) {
            const directions = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw'];
            directions.forEach(dir => {
                const handle = document.createElement('div');
                handle.className = `resize-handle resize-${dir}`;
                el.appendChild(handle);
                
                handle.addEventListener('mousedown', (e) => startResize(e, dir));
                handle.addEventListener('touchstart', (e) => startResize(e, dir), { passive: false });
            });
        }
        
        function addRotateHandle(el) {
            const handle = document.createElement('div');
            handle.className = 'rotate-corner';
            handle.title = 'Вращать';
            el.appendChild(handle);
            
            const indicator = document.createElement('div');
            indicator.className = 'rotate-indicator';
            indicator.textContent = '0°';
            el.appendChild(indicator);
            
            handle.addEventListener('mousedown', startRotate);
            handle.addEventListener('touchstart', startRotate, { passive: false });
        }
        
        function startImageDrag(e) {
            if (e.target.classList.contains('resize-handle') || e.target.classList.contains('rotate-corner')) return;
            e.preventDefault();
            
            const el = e.currentTarget;
            if (el.classList.contains('locked')) return;
            
            selectImage(el.id);
            
            activeInteraction = 'drag';
            activeElement = el;
            
            const rect = el.getBoundingClientRect();
            const clientX = e.type === 'touchstart' ? e.touches[0].clientX : e.clientX;
            const clientY = e.type === 'touchstart' ? e.touches[0].clientY : e.clientY;
            
            startX = clientX - rect.left;
            startY = clientY - rect.top;
        }
        
        function startTextDrag(e) {
            if (e.target.classList.contains('resize-handle')) return;
            e.preventDefault();
            
            const el = e.currentTarget;
            if (el.classList.contains('locked')) return;
            
            selectText(el.id);
            
            activeInteraction = 'drag';
            activeElement = el;
            
            const rect = el.getBoundingClientRect();
            const clientX = e.type === 'touchstart' ? e.touches[0].clientX : e.clientX;
            const clientY = e.type === 'touchstart' ? e.touches[0].clientY : e.clientY;
            
            startX = clientX - rect.left;
            startY = clientY - rect.top;
        }
        
        function startWidgetDrag(e) {
            if (e.target.classList.contains('resize-handle')) return;
            e.preventDefault();
            
            const el = e.currentTarget;
            if (el.classList.contains('locked')) return;
            
            selectWidget(el.id);
            
            activeInteraction = 'drag';
            activeElement = el;
            
            const rect = el.getBoundingClientRect();
            const clientX = e.type === 'touchstart' ? e.touches[0].clientX : e.clientX;
            const clientY = e.type === 'touchstart' ? e.touches[0].clientY : e.clientY;
            
            startX = clientX - rect.left;
            startY = clientY - rect.top;
        }
        
        function startResize(e, direction) {
            e.preventDefault();
            e.stopPropagation();
            
            const el = e.currentTarget.parentElement;
            if (el.classList.contains('locked')) return;
            
            activeInteraction = 'resize';
            activeElement = el;
            resizeDirection = direction;
            
            const rect = el.getBoundingClientRect();
            startX = e.type === 'touchstart' ? e.touches[0].clientX : e.clientX;
            startY = e.type === 'touchstart' ? e.touches[0].clientY : e.clientY;
            
            startWidth = rect.width;
            startHeight = rect.height;
            startLeft = rect.left;
            startTop = rect.top;
        }
        
        function startRotate(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const el = e.currentTarget.parentElement;
            if (el.classList.contains('locked')) return;
            
            activeInteraction = 'rotate';
            activeElement = el;
            
            const rect = el.getBoundingClientRect();
            startX = e.type === 'touchstart' ? e.touches[0].clientX : e.clientX;
            startY = e.type === 'touchstart' ? e.touches[0].clientY : e.clientY;
            
            startRotation = parseFloat(el.dataset.rotation) || 0;
        }
        
        function handleMove(e) {
            if (!activeInteraction || !activeElement) return;
            e.preventDefault();
            
            const clientX = e.type === 'touchmove' ? e.touches[0].clientX : e.clientX;
            const clientY = e.type === 'touchmove' ? e.touches[0].clientY : e.clientY;
            
            if (activeInteraction === 'drag') {
                const container = document.getElementById('canvas-wrapper').querySelector('.canvas-content');
                const newX = clientX - startX;
                const newY = clientY - startY;
                
                const maxX = container.offsetWidth - activeElement.offsetWidth;
                const maxY = container.offsetHeight - activeElement.offsetHeight;
                
                activeElement.style.left = Math.max(0, Math.min(newX, maxX)) + 'px';
                activeElement.style.top = Math.max(0, Math.min(newY, maxY)) + 'px';
                
                savePosition();
            }
            else if (activeInteraction === 'resize') {
                const deltaX = clientX - startX;
                const deltaY = clientY - startY;
                
                let newWidth = startWidth;
                let newHeight = startHeight;
                let newLeft = startLeft;
                let newTop = startTop;
                
                switch (resizeDirection) {
                    case 'e': newWidth = Math.max(20, startWidth + deltaX); break;
                    case 'w': newWidth = Math.max(20, startWidth - deltaX); newLeft = startLeft + (startWidth - newWidth); break;
                    case 's': newHeight = Math.max(20, startHeight + deltaY); break;
                    case 'n': newHeight = Math.max(20, startHeight - deltaY); newTop = startTop + (startHeight - newHeight); break;
                    case 'se': newWidth = Math.max(20, startWidth + deltaX); newHeight = Math.max(20, startHeight + deltaY); break;
                    case 'sw': newWidth = Math.max(20, startWidth - deltaX); newHeight = Math.max(20, startHeight + deltaY); newLeft = startLeft + (startWidth - newWidth); break;
                    case 'ne': newWidth = Math.max(20, startWidth + deltaX); newHeight = Math.max(20, startHeight - deltaY); newTop = startTop + (startHeight - newHeight); break;
                    case 'nw': newWidth = Math.max(20, startWidth - deltaX); newHeight = Math.max(20, startHeight - deltaY); newLeft = startLeft + (startWidth - newWidth); newTop = startTop + (startHeight - newHeight); break;
                }
                
                activeElement.style.width = newWidth + 'px';
                activeElement.style.height = newHeight + 'px';
                activeElement.style.left = newLeft + 'px';
                activeElement.style.top = newTop + 'px';
                
                saveSize();
            }
            else if (activeInteraction === 'rotate') {
                const rect = activeElement.getBoundingClientRect();
                const centerX = rect.left + rect.width / 2;
                const centerY = rect.top + rect.height / 2;
                
                const angle = Math.atan2(clientY - centerY, clientX - centerX) * 180 / Math.PI;
                const startAngle = Math.atan2(startY - centerY, startX - centerX) * 180 / Math.PI;
                let deltaAngle = angle - startAngle;
                
                if (deltaAngle > 180) deltaAngle -= 360;
                if (deltaAngle < -180) deltaAngle += 360;
                
                const newRotation = Math.round(startRotation + deltaAngle);
                activeElement.dataset.rotation = newRotation;
                applyTransformations(activeElement);
                
                const indicator = activeElement.querySelector('.rotate-indicator');
                if (indicator) indicator.textContent = newRotation + '°';
                
                saveRotation();
            }
        }
        
        function savePosition() {
            if (!activeElement) return;
            const id = activeElement.id;
            const x = parseInt(activeElement.style.left) || 0;
            const y = parseInt(activeElement.style.top) || 0;
            
            if (images[id]) imagesRef.child(id).update({ x, y });
            else if (texts[id]) textsRef.child(id).update({ x, y });
            else if (widgets[id]) widgetsRef.child(id).update({ x, y });
        }
        
        function saveSize() {
            if (!activeElement) return;
            const id = activeElement.id;
            const x = parseInt(activeElement.style.left) || 0;
            const y = parseInt(activeElement.style.top) || 0;
            const width = parseInt(activeElement.style.width) || activeElement.offsetWidth;
            const height = parseInt(activeElement.style.height) || activeElement.offsetHeight;
            
            if (images[id]) imagesRef.child(id).update({ x, y, width, height });
            else if (texts[id]) textsRef.child(id).update({ x, y });
            else if (widgets[id]) widgetsRef.child(id).update({ x, y, width, height });
        }
        
        function saveRotation() {
            if (!activeElement) return;
            const id = activeElement.id;
            const rotation = parseInt(activeElement.dataset.rotation) || 0;
            
            if (images[id]) imagesRef.child(id).update({ rotation });
        }
        
        function endInteraction() {
            if (activeInteraction) saveStateToHistory();
            activeInteraction = null;
            activeElement = null;
        }
        
        function applyTransformations(el) {
            let transform = '';
            const rotation = el.dataset.rotation || 0;
            if (rotation && rotation !== '0') transform += `rotate(${rotation}deg) `;
            if (el.dataset.flipH === 'true') transform += 'scaleX(-1) ';
            if (el.dataset.flipV === 'true') transform += 'scaleY(-1) ';
            el.style.transform = transform.trim();
        }
        
        function updateThumbnails() {
            const container = document.getElementById('thumbnails');
            container.innerHTML = '';
            
            // Изображения
            for (const id in images) {
                const data = images[id];
                const thumb = document.createElement('div');
                thumb.className = 'thumbnail';
                if (data.display === 'none') thumb.classList.add('thumbnail-hidden');
                if (selectedImageId === id) thumb.classList.add('selected');
                
                const img = document.createElement('img');
                img.src = data.src;
                thumb.appendChild(img);
                
                const btn = document.createElement('button');
                btn.className = 'thumbnail-button' + (data.display === 'none' ? ' show' : '');
                btn.textContent = data.display === 'none' ? '👁' : '✕';
                btn.onclick = (e) => {
                    e.stopPropagation();
                    toggleVisibility(id, 'image', data.display !== 'none');
                };
                thumb.appendChild(btn);
                
                thumb.onclick = () => selectImage(id);
                container.appendChild(thumb);
            }
            
            // Тексты
            for (const id in texts) {
                const data = texts[id];
                const thumb = document.createElement('div');
                thumb.className = 'thumbnail';
                if (data.display === 'none') thumb.classList.add('thumbnail-hidden');
                if (selectedTextId === id) thumb.classList.add('selected');
                
                const preview = document.createElement('div');
                preview.className = 'text-thumbnail';
                preview.textContent = (data.text || 'Текст').substring(0, 10) + '...';
                preview.style.color = data.color || '#000';
                thumb.appendChild(preview);
                
                const btn = document.createElement('button');
                btn.className = 'thumbnail-button' + (data.display === 'none' ? ' show' : '');
                btn.textContent = data.display === 'none' ? '👁' : '✕';
                btn.onclick = (e) => {
                    e.stopPropagation();
                    toggleVisibility(id, 'text', data.display !== 'none');
                };
                thumb.appendChild(btn);
                
                thumb.onclick = () => selectText(id);
                container.appendChild(thumb);
            }
            
            // Звуки
            for (const id in sounds) {
                const data = sounds[id];
                const thumb = document.createElement('div');
                thumb.className = 'thumbnail';
                if (data.display === 'none') thumb.classList.add('thumbnail-hidden');
                if (selectedSoundId === id) thumb.classList.add('selected');
                
                const preview = document.createElement('div');
                preview.className = 'sound-thumbnail';
                preview.textContent = (data.name || 'Звук').substring(0, 10) + '...';
                thumb.appendChild(preview);
                
                const btn = document.createElement('button');
                btn.className = 'thumbnail-button' + (data.display === 'none' ? ' show' : '');
                btn.textContent = data.display === 'none' ? '👁' : '✕';
                btn.onclick = (e) => {
                    e.stopPropagation();
                    toggleVisibility(id, 'sound', data.display !== 'none');
                };
                thumb.appendChild(btn);
                
                thumb.onclick = () => selectSound(id);
                container.appendChild(thumb);
            }
            
            // Виджеты
            for (const id in widgets) {
                const data = widgets[id];
                const thumb = document.createElement('div');
                thumb.className = 'thumbnail';
                if (data.display === 'none') thumb.classList.add('thumbnail-hidden');
                if (selectedWidgetId === id) thumb.classList.add('selected');
                
                const preview = document.createElement('div');
                preview.className = 'widget-thumbnail';
                preview.textContent = (data.name || 'Виджет').substring(0, 10) + '...';
                thumb.appendChild(preview);
                
                const btn = document.createElement('button');
                btn.className = 'thumbnail-button' + (data.display === 'none' ? ' show' : '');
                btn.textContent = data.display === 'none' ? '👁' : '✕';
                btn.onclick = (e) => {
                    e.stopPropagation();
                    toggleVisibility(id, 'widget', data.display !== 'none');
                };
                thumb.appendChild(btn);
                
                thumb.onclick = () => selectWidget(id);
                container.appendChild(thumb);
            }
        }
        
        function toggleVisibility(id, type, hide) {
            const newDisplay = hide ? 'none' : 'block';
            const el = document.getElementById(id);
            if (el) el.style.display = newDisplay;
            
            if (type === 'image') imagesRef.child(id).update({ display: newDisplay });
            else if (type === 'text') textsRef.child(id).update({ display: newDisplay });
            else if (type === 'sound') soundsRef.child(id).update({ display: newDisplay });
            else if (type === 'widget') widgetsRef.child(id).update({ display: newDisplay });
            
            updateThumbnails();
        }
        
        function toggleImageVisibility() {
            if (selectedImageId) toggleVisibility(selectedImageId, 'image', document.getElementById(selectedImageId).style.display !== 'none');
        }
        
        function deleteSelectedImage() {
            if (selectedImageId && confirm('Удалить изображение?')) {
                imagesRef.child(selectedImageId).remove();
                deselectAll();
            }
        }
        
        function showImageProperties() {
            if (selectedImageId) {
                document.getElementById('properties-panel').style.display = 'block';
            }
        }
        
        function toggleImageLock() {
            if (!selectedImageId) return;
            const el = document.getElementById(selectedImageId);
            const locked = !el.classList.contains('locked');
            el.classList.toggle('locked', locked);
            document.getElementById('lock-btn').textContent = locked ? '🔓 Открепить' : '🔒 Закрепить';
            imagesRef.child(selectedImageId).update({ locked });
        }
        
        function flipImage(direction) {
            if (!selectedImageId) return;
            const el = document.getElementById(selectedImageId);
            const prop = direction === 'horizontal' ? 'flipH' : 'flipV';
            const current = el.dataset[prop] === 'true';
            el.dataset[prop] = (!current).toString();
            applyTransformations(el);
            imagesRef.child(selectedImageId).update({ [direction === 'horizontal' ? 'flipHorizontal' : 'flipVertical']: !current });
        }
        
        function toggleTextVisibility() {
            if (selectedTextId) toggleVisibility(selectedTextId, 'text', document.getElementById(selectedTextId).style.display !== 'none');
        }
        
        function deleteSelectedText() {
            if (selectedTextId && confirm('Удалить текст?')) {
                textsRef.child(selectedTextId).remove();
                deselectAll();
            }
        }
        
        function toggleTextLock() {
            if (!selectedTextId) return;
            const el = document.getElementById(selectedTextId);
            const locked = !el.classList.contains('locked');
            el.classList.toggle('locked', locked);
            document.getElementById('lock-text-btn').textContent = locked ? '🔓 Открепить' : '🔒 Закрепить';
            textsRef.child(selectedTextId).update({ locked });
        }
        
        function toggleWidgetVisibility() {
            if (selectedWidgetId) toggleVisibility(selectedWidgetId, 'widget', document.getElementById(selectedWidgetId).style.display !== 'none');
        }
        
        function deleteSelectedWidget() {
            if (selectedWidgetId && confirm('Удалить виджет?')) {
                widgetsRef.child(selectedWidgetId).remove();
                deselectAll();
            }
        }
        
        function toggleWidgetLock() {
            if (!selectedWidgetId) return;
            const el = document.getElementById(selectedWidgetId);
            const locked = !el.classList.contains('locked');
            el.classList.toggle('locked', locked);
            document.getElementById('lock-widget-btn').textContent = locked ? '🔓 Открепить' : '🔒 Закрепить';
            widgetsRef.child(selectedWidgetId).update({ locked });
        }
        
        function reloadSelectedWidget() {
            if (selectedWidgetId) {
                const iframe = document.getElementById(selectedWidgetId)?.querySelector('iframe');
                if (iframe) iframe.src = iframe.src;
            }
        }
        
        function showSimpleTextInput() {
            deselectAll();
            const panel = document.getElementById('simple-text-input');
            panel.style.display = 'block';
            document.getElementById('text-input-area').value = '';
            isAddingText = true;
        }
        
        function updateTextPreview() {
            const textarea = document.getElementById('text-input-area');
            textarea.style.fontSize = document.getElementById('font-size-slider').value + 'px';
            textarea.style.color = document.getElementById('text-color-picker').value;
            textarea.style.fontFamily = document.getElementById('font-family-select').value;
        }
        
        function createTextFromSimpleInput() {
            const text = document.getElementById('text-input-area').value.trim();
            if (!text) {
                alert('Введите текст');
                return;
            }
            
            const id = 'text_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            const panel = document.getElementById('simple-text-input');
            const rect = panel.getBoundingClientRect();
            
            textsRef.child(id).set({
                id,
                text,
                x: 100,
                y: 100,
                fontSize: parseInt(document.getElementById('font-size-slider').value) || 16,
                color: document.getElementById('text-color-picker').value,
                fontFamily: document.getElementById('font-family-select').value,
                opacity: 1,
                isNew: true,
                locked: false,
                display: 'block'
            });
            
            panel.style.display = 'none';
            isAddingText = false;
        }
        
        function cancelSimpleTextInput() {
            document.getElementById('simple-text-input').style.display = 'none';
            isAddingText = false;
        }
        
        function editSelectedText() {
            if (!selectedTextId) return;
            const el = document.getElementById(selectedTextId);
            if (!el) return;
            
            const panel = document.getElementById('simple-text-input');
            const textarea = document.getElementById('text-input-area');
            
            textarea.value = el.textContent || '';
            textarea.style.fontSize = el.style.fontSize;
            textarea.style.color = el.style.color;
            textarea.style.fontFamily = el.style.fontFamily;
            
            document.getElementById('font-size-slider').value = parseInt(el.style.fontSize) || 16;
            document.getElementById('text-color-picker').value = el.style.color || '#000000';
            document.getElementById('font-family-select').value = el.style.fontFamily || "'Comic Sans MS', cursive";
            
            panel.style.display = 'block';
            isAddingText = true;
            
            document.getElementById('apply-text-simple').onclick = function() {
                const newText = textarea.value.trim();
                if (!newText) return;
                
                textsRef.child(selectedTextId).update({
                    text: newText,
                    fontSize: parseInt(document.getElementById('font-size-slider').value) || 16,
                    color: document.getElementById('text-color-picker').value,
                    fontFamily: document.getElementById('font-family-select').value
                });
                
                panel.style.display = 'none';
                isAddingText = false;
                document.getElementById('apply-text-simple').onclick = createTextFromSimpleInput;
            };
        }
        
        function showWidgetsPanel() {
            document.getElementById('widgets-panel').style.display = 'block';
            isAddingWidget = true;
        }
        
        function closeWidgetsPanel() {
            document.getElementById('widgets-panel').style.display = 'none';
            isAddingWidget = false;
        }
        
        function saveWidgetFromInput() {
            const url = document.getElementById('widget-url-input').value.trim();
            const width = parseInt(document.getElementById('widget-width-input').value) || 400;
            const height = parseInt(document.getElementById('widget-height-input').value) || 300;
            const name = document.getElementById('widget-name-input').value.trim() || 'Виджет';
            
            if (!url) {
                alert('Введите URL');
                return;
            }
            
            try {
                new URL(url);
            } catch {
                alert('Некорректный URL');
                return;
            }
            
            savedWidgetsRef.push({
                url,
                name,
                width,
                height,
                timestamp: Date.now()
            }).then(() => {
                alert('Виджет сохранен');
            });
        }
        
        function addWidgetDirectly() {
            const url = document.getElementById('widget-url-input').value.trim();
            const width = parseInt(document.getElementById('widget-width-input').value) || 400;
            const height = parseInt(document.getElementById('widget-height-input').value) || 300;
            const name = document.getElementById('widget-name-input').value.trim() || 'Виджет';
            
            if (!url) {
                alert('Введите URL');
                return;
            }
            
            try {
                new URL(url);
            } catch {
                alert('Некорректный URL');
                return;
            }
            
            const id = 'widget_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            widgetsRef.child(id).set({
                id,
                url,
                name,
                x: 100,
                y: 100,
                width,
                height,
                opacity: 1,
                locked: false,
                display: 'block',
                isNew: true
            });
            
            closeWidgetsPanel();
        }
        
        function updateSavedWidgetsList() {
            const list = document.getElementById('saved-widgets-list');
            list.innerHTML = '';
            
            if (Object.keys(savedWidgets).length === 0) {
                list.innerHTML = '<p style="text-align: center; color: #666;">Нет сохраненных виджетов</p>';
                return;
            }
            
            Object.values(savedWidgets).forEach(widget => {
                const item = document.createElement('div');
                item.className = 'saved-widget-item';
                
                const name = document.createElement('span');
                name.className = 'saved-widget-name';
                name.textContent = widget.name;
                name.title = widget.url;
                
                const actions = document.createElement('div');
                actions.className = 'widget-actions';
                
                const addBtn = document.createElement('button');
                addBtn.className = 'widget-action-btn add-widget-btn';
                addBtn.textContent = '+';
                addBtn.onclick = () => {
                    const id = 'widget_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
                    widgetsRef.child(id).set({
                        id,
                        url: widget.url,
                        name: widget.name,
                        x: 100,
                        y: 100,
                        width: widget.width,
                        height: widget.height,
                        opacity: 1,
                        locked: false,
                        display: 'block',
                        isNew: true
                    });
                };
                
                const delBtn = document.createElement('button');
                delBtn.className = 'widget-action-btn remove-widget-btn';
                delBtn.textContent = '×';
                delBtn.onclick = () => {
                    if (confirm('Удалить сохраненный виджет?')) {
                        savedWidgetsRef.child(widget.id).remove();
                    }
                };
                
                actions.appendChild(addBtn);
                actions.appendChild(delBtn);
                
                item.appendChild(name);
                item.appendChild(actions);
                list.appendChild(item);
            });
        }
        
        function handleFileUpload(e) {
            const file = e.target.files[0];
            if (!file) return;
            
            const reader = new FileReader();
            reader.onload = (event) => {
                const img = new Image();
                img.onload = () => {
                    const id = 'img_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
                    imagesRef.child(id).set({
                        id,
                        src: event.target.result,
                        x: 100,
                        y: 100,
                        width: img.width,
                        height: img.height,
                        opacity: 1,
                        brightness: 100,
                        rotation: 0,
                        flipHorizontal: false,
                        flipVertical: false,
                        isNew: true,
                        locked: false,
                        display: 'block'
                    });
                };
                img.src = event.target.result;
            };
            reader.readAsDataURL(file);
            e.target.value = '';
        }
        
        function handleSoundUpload(e) {
            const file = e.target.files[0];
            if (!file) return;
            
            const reader = new FileReader();
            reader.onload = (event) => {
                const id = 'sound_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
                soundsRef.child(id).set({
                    id,
                    src: event.target.result,
                    name: file.name,
                    playing: false,
                    currentTime: 0,
                    duration: 0,
                    volume: 100,
                    display: 'block'
                });
            };
            reader.readAsDataURL(file);
            e.target.value = '';
        }
        
        function updateSoundControls(data) {
            const audio = document.getElementById('audio-element');
            if (audio.src !== data.src) {
                audio.src = data.src;
                audio.onloadedmetadata = () => {
                    soundsRef.child(selectedSoundId).update({ duration: audio.duration });
                };
            }
            
            audio.volume = (data.volume || 100) / 100;
            document.getElementById('volume-slider').value = data.volume || 100;
            
            if (data.playing && audio.paused) {
                audio.currentTime = data.currentTime || 0;
                audio.play().catch(() => {});
            } else if (!data.playing && !audio.paused) {
                audio.pause();
            }
            
            updateProgressVisualization(data.currentTime, data.duration);
        }
        
        function playSound() {
            if (!selectedSoundId) return;
            const audio = document.getElementById('audio-element');
            audio.play().then(() => {
                soundsRef.child(selectedSoundId).update({ playing: true });
                if (soundInterval) clearInterval(soundInterval);
                soundInterval = setInterval(() => {
                    soundsRef.child(selectedSoundId).update({ currentTime: audio.currentTime });
                }, 1000);
            });
        }
        
        function pauseSound() {
            if (!selectedSoundId) return;
            const audio = document.getElementById('audio-element');
            audio.pause();
            soundsRef.child(selectedSoundId).update({ playing: false });
            if (soundInterval) {
                clearInterval(soundInterval);
                soundInterval = null;
            }
        }
        
        function deleteSound() {
            if (selectedSoundId && confirm('Удалить звук?')) {
                soundsRef.child(selectedSoundId).remove();
                document.getElementById('audio-element').pause();
                if (soundInterval) clearInterval(soundInterval);
                deselectAll();
            }
        }
        
        function updateVolume(e) {
            if (!selectedSoundId) return;
            const volume = e.target.value;
            document.getElementById('audio-element').volume = volume / 100;
            soundsRef.child(selectedSoundId).update({ volume });
        }
        
        function updateProgressVisualization(currentTime, duration) {
            const progress = document.getElementById('sound-progress');
            if (duration > 0) {
                progress.style.width = (currentTime / duration * 100) + '%';
            }
        }
        
        function showTTSPanel() {
            document.getElementById('tts-panel').style.display = 'block';
            initTTS();
        }
        
        function closeTTSPanel() {
            document.getElementById('tts-panel').style.display = 'none';
            stopTTS();
        }
        
        function initTTS() {
            if ('speechSynthesis' in window) {
                speechSynthesis.onvoiceschanged = () => {
                    voices = speechSynthesis.getVoices();
                    populateVoiceList();
                };
                voices = speechSynthesis.getVoices();
                if (voices.length > 0) populateVoiceList();
                isTTSInitialized = true;
            }
        }
        
        function populateVoiceList() {
            const select = document.getElementById('tts-voice-select');
            select.innerHTML = '<option value="">Выберите голос...</option>';
            
            const russianVoices = voices.filter(v => 
                v.lang.startsWith('ru') || v.name.toLowerCase().includes('russian')
            );
            
            (russianVoices.length ? russianVoices : voices).forEach(voice => {
                const option = document.createElement('option');
                option.value = voice.name;
                option.textContent = `${voice.name} (${voice.lang})`;
                select.appendChild(option);
            });
        }
        
        function playTTS() {
            const text = document.getElementById('tts-text-input').value.trim();
            if (!text) return alert('Введите текст');
            
            if (speechSynthesis.speaking) speechSynthesis.cancel();
            
            speechUtterance = new SpeechSynthesisUtterance(text);
            
            const voiceSelect = document.getElementById('tts-voice-select');
            const selectedVoice = voices.find(v => v.name === voiceSelect.value);
            if (selectedVoice) speechUtterance.voice = selectedVoice;
            
            speechUtterance.rate = parseFloat(document.getElementById('tts-rate-slider').value);
            speechUtterance.pitch = parseFloat(document.getElementById('tts-pitch-slider').value);
            speechUtterance.volume = parseFloat(document.getElementById('tts-volume-slider').value);
            
            speechSynthesis.speak(speechUtterance);
        }
        
        function pauseTTS() {
            if (speechSynthesis.speaking) speechSynthesis.pause();
        }
        
        function stopTTS() {
            speechSynthesis.cancel();
        }
        
        function startCrop(type) {
            let id = null;
            if (type === 'image' && selectedImageId) id = selectedImageId;
            else if (type === 'text' && selectedTextId) id = selectedTextId;
            else if (type === 'widget' && selectedWidgetId) id = selectedWidgetId;
            
            if (!id) {
                alert('Выберите элемент');
                return;
            }
            
            cropMode = true;
            cropElement = document.getElementById(id);
            cropType = type;
            
            document.getElementById('crop-panel').style.display = 'block';
            document.getElementById('crop-width').value = cropElement.offsetWidth;
            document.getElementById('crop-height').value = cropElement.offsetHeight;
            
            updateCropPreview();
        }
        
        function updateCropPreview() {
            const preview = document.getElementById('crop-preview');
            preview.innerHTML = '';
            
            if (!cropElement) return;
            
            if (cropType === 'image') {
                const img = cropElement.querySelector('img');
                if (img) {
                    const clone = img.cloneNode();
                    clone.style.maxWidth = '100%';
                    clone.style.maxHeight = '100%';
                    preview.appendChild(clone);
                }
            } else if (cropType === 'text') {
                const div = document.createElement('div');
                div.textContent = cropElement.textContent;
                div.style.cssText = cropElement.style.cssText;
                div.style.padding = '10px';
                preview.appendChild(div);
            } else if (cropType === 'widget') {
                const div = document.createElement('div');
                div.textContent = '🧩 ' + (widgets[cropElement.id]?.name || 'Виджет');
                div.style.padding = '20px';
                div.style.background = '#e8f5e9';
                div.style.color = '#2e7d32';
                div.style.textAlign = 'center';
                preview.appendChild(div);
            }
        }
        
        function applyCrop() {
            if (!cropMode || !cropElement) return;
            
            const x = parseInt(document.getElementById('crop-x').value) || 0;
            const y = parseInt(document.getElementById('crop-y').value) || 0;
            const w = parseInt(document.getElementById('crop-width').value) || 10;
            const h = parseInt(document.getElementById('crop-height').value) || 10;
            
            const crop = { x, y, width: w, height: h };
            
            if (cropType === 'image') {
                cropElement.style.clipPath = `inset(${y}px ${cropElement.offsetWidth - x - w}px ${cropElement.offsetHeight - y - h}px ${x}px)`;
                imagesRef.child(cropElement.id).update({ crop });
            } else if (cropType === 'text') {
                cropElement.style.overflow = 'hidden';
                cropElement.style.maxWidth = w + 'px';
                cropElement.style.maxHeight = h + 'px';
                textsRef.child(cropElement.id).update({ crop });
            } else if (cropType === 'widget') {
                cropElement.style.clipPath = `inset(${y}px ${cropElement.offsetWidth - x - w}px ${cropElement.offsetHeight - y - h}px ${x}px)`;
                widgetsRef.child(cropElement.id).update({ crop });
            }
            
            cancelCrop();
        }
        
        function cancelCrop() {
            cropMode = false;
            cropElement = null;
            cropType = null;
            document.getElementById('crop-panel').style.display = 'none';
        }
        
        function clearCanvas() {
            if (confirm('Очистить холст?')) {
                imagesRef.remove();
                textsRef.remove();
                soundsRef.remove();
                widgetsRef.remove();
                deselectAll();
            }
        }
        
        function saveStateToHistory() {
            if (actionHistory.length >= 20) actionHistory.shift();
            
            Promise.all([
                imagesRef.once('value').then(s => s.val() || {}),
                textsRef.once('value').then(s => s.val() || {}),
                soundsRef.once('value').then(s => s.val() || {}),
                widgetsRef.once('value').then(s => s.val() || {})
            ]).then(([i, t, s, w]) => {
                actionHistory.push(JSON.stringify({ images: i, texts: t, sounds: s, widgets: w }));
                historyPointer = actionHistory.length - 1;
            });
        }
        
        function undoAction() {
            if (historyPointer <= 0) return;
            historyPointer--;
            const state = JSON.parse(actionHistory[historyPointer]);
            imagesRef.set(state.images || {});
            textsRef.set(state.texts || {});
            soundsRef.set(state.sounds || {});
            widgetsRef.set(state.widgets || {});
        }
        
        window.addEventListener('DOMContentLoaded', initApp);
    </script>
</body>
</html>
