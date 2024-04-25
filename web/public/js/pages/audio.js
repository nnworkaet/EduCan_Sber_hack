let lastData = null;

function deepEqual(object1, object2) {
    const keys1 = Object.keys(object1);
    const keys2 = Object.keys(object2);

    if (keys1.length !== keys2.length) {
        return false;
    }

    for (const key of keys1) {
        const val1 = object1[key];
        const val2 = object2[key];
        const areObjects = isObject(val1) && isObject(val2);
        if (
            areObjects && !deepEqual(val1, val2) ||
            !areObjects && val1 !== val2
        ) {
            return false;
        }
    }

    return true;
}

function isObject(object) {
    return object != null && typeof object === 'object';
}

function checkForUpdates() {
    getFullInformationForInitialRender().then(newData => {
        if (!lastData || !deepEqual(lastData, newData)) {
            lastData = newData;
            rerenderAllInformation();
        }
    }).catch(error => {
        console.error('Ошибка при получении данных: ', error);
    });
}

$(document).on('click', '.save-edits-transcribing', function() {
    let transcribingTextarea = $(".transcribing-textarea").val().trim();

    $.ajax({
        type: "POST",
        data: {
            identity: localStorage.getItem("selectedAudioId"),
            textTranscription: transcribingTextarea
        },
        url: "./src/Api/v1.php?saveEditsTranscribing",
        success: function(data) {
            appendDivWithScript(data);
        }
    });
});

$(document).on('click', '.save-edits-summary', function() {
    let summaryTextarea = $(".summary-textarea").val().trim();

    $.ajax({
        type: "POST",
        data: {
            identity: localStorage.getItem("selectedAudioId"),
            textSummary: summaryTextarea
        },
        url: "./src/Api/v1.php?saveEditsSummary",
        success: function(data) {
            appendDivWithScript(data);
        }
    });
});

$(document).on('click', '.download-test', function() {
    getFullInformationForInitialRender().then((data) => {
        console.log(data["text_test"])
        downloadTest(data["text_test"]);
    });
});

$(document).on('click', '.download-summary', function() {
    var filename = $(this).attr('file-name');
    if (filename) {
        window.location.href = '/temp/' + filename;
    } else {
        console.error('Filename не найден');
    }
});

function getFullInformationForInitialRender() {
    return new Promise((resolve, reject) => {
        $.ajax({
            type: "POST",
            data: {
                identity: localStorage.getItem("selectedAudioId")
            },
            url: "./src/Api/v1.php?getFullInformationForInitialRender",
            success: function(data) {
                resolve(data);
            },
            error: function(error) {
                reject(error);
            }
        });
    });
}

function appendTitle(title) {
    $(".lecture-name").html(title);
}

function getAudioType(fileName) {
    var extension = fileName.split('.').pop().toLowerCase();
    var types = {
        'mp3': 'audio/mpeg',
        'ogg': 'audio/ogg',
        'wav': 'audio/wav',
        'aac': 'audio/aac',
        'm4a': 'audio/x-m4a'
    };

    return types[extension] || 'audio/mpeg';
}

function appendAudio(audioName) {
    var audioType = getAudioType(audioName);
    var audioElement = `
        <audio controls class="audio-object w-full">
            <source src="./temp/${audioName}" type="${audioType}">
            Ваш браузер не поддерживает элемент <code>audio</code>.
        </audio>
    `;
    $(".audio-container").html(audioElement);
}

function appendSteps(transcription, summary, glossary, test) {

    let renderObject = `<span class="inline-flex items-center gap-x-1.5 rounded-md bg-green-100 px-4 py-1 text-xs font-medium text-green-700">
    Аудио загружено
    <svg class="h-3 w-3 text-green-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5"></path>
    </svg>
</span> `;

    if(transcription == null || transcription == "" || transcription == undefined) {
        renderObject += `<span class="inline-flex items-center gap-x-1.5 rounded-md bg-red-100 px-4 py-1 text-xs font-medium text-red-700">
        Транскрибация сделана
            <svg class="h-3 w-3 text-red-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
        </span>`;
    } else {
        renderObject += `<span class="inline-flex items-center gap-x-1.5 rounded-md bg-green-100 px-4 py-1 text-xs font-medium text-green-700">
        Транскрибация сделана
        <svg class="h-3 w-3 text-green-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5"></path>
        </svg>
    </span>`;
    }

    if(summary == null || summary == "" || summary == undefined) {
        renderObject += `<span class="inline-flex items-center gap-x-1.5 rounded-md bg-red-100 px-4 py-1 text-xs font-medium text-red-700">
        Конспект сделан
            <svg class="h-3 w-3 text-red-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
        </span>`;
    } else {
        renderObject += `<span class="inline-flex items-center gap-x-1.5 rounded-md bg-green-100 px-4 py-1 text-xs font-medium text-green-700">
        Конспект сделан
        <svg class="h-3 w-3 text-green-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5"></path>
        </svg>
    </span>`;
    }

    if(glossary == null || glossary == "" || glossary == undefined) {
        renderObject += `<span class="inline-flex items-center gap-x-1.5 rounded-md bg-red-100 px-4 py-1 text-xs font-medium text-red-700">
        Глоссарий составлен
            <svg class="h-3 w-3 text-red-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
        </span>`;
    } else {
        renderObject += `<span class="inline-flex items-center gap-x-1.5 rounded-md bg-green-100 px-4 py-1 text-xs font-medium text-green-700">
        Глоссарий составлен
        <svg class="h-3 w-3 text-green-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5"></path>
        </svg>
    </span>`;
    }

    if(test == null || test == "" || test == undefined) {
        renderObject += `<span class="inline-flex items-center gap-x-1.5 rounded-md bg-red-100 px-4 py-1 text-xs font-medium text-red-700">
        Тест составлен
            <svg class="h-3 w-3 text-red-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
        </span>`;
    } else {
        renderObject += `<span class="inline-flex items-center gap-x-1.5 rounded-md bg-green-100 px-4 py-1 text-xs font-medium text-green-700">
        Тест составлен
        <svg class="h-3 w-3 text-green-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5"></path>
        </svg>
    </span>`;
    }
    
    $(".audio-steps-object").html(renderObject);
}

getFullInformationForInitialRender().then((data) => {
    appendTitle(data["lecture_name"]);
    appendAudio(data["audio_name"]);
    appendSteps(data["text_transcription"], data["text_summary"], data["text_glossary"], data["text_test"]);

    renderTranscribingBlock(data["text_transcription"]);
    renderSummaryBlock(data["text_summary"], data["filename_summary"]);
    renderGlossaryBlock(data["text_glossary"]);
    renderTestBlock(data["text_test"]);
});

$(document).ready(() => {
    initListeners();
});

function initListeners() {
    $(".start-transcription").click(() => {
        $.ajax({
            type: "POST",
            data: {
                identity: localStorage.getItem("selectedAudioId")
            },
            url: "./src/Api/v1.php?startTranscription",
            success: function(data) {
                appendDivWithScript(data);
            }
        });
    });

    $(".start-summary").click(() => {
        getFullInformationForInitialRender().then((data) => {
            if(data["text_transcription"] != null) {
                $.ajax({
                    type: "POST",
                    data: {
                        identity: localStorage.getItem("selectedAudioId")
                    },
                    url: "./src/Api/v1.php?startSummary",
                    success: function(data) {
                        appendDivWithScript(data);
                    }
                });
            } else {
                addNotification("Ошибка работы", "Сначала сделайте транскрибацию!", "Danger");
            }
        });
    });

    $(".start-glossary").click(() => {
        getFullInformationForInitialRender().then((data) => {
            if(data["text_transcription"] != null) {
                $.ajax({
                    type: "POST",
                    data: {
                        identity: localStorage.getItem("selectedAudioId")
                    },
                    url: "./src/Api/v1.php?startGlossary",
                    success: function(data) {
                        appendDivWithScript(data);
                    }
                });
            } else {
                addNotification("Ошибка работы", "Сначала сделайте транскрибацию!", "Danger");
            }
        });
    });

    $(".start-test").click(() => {
        getFullInformationForInitialRender().then((data) => {
            if(data["text_transcription"] != null && data["text_summary"] != null) {
                $.ajax({
                    type: "POST",
                    data: {
                        identity: localStorage.getItem("selectedAudioId")
                    },
                    url: "./src/Api/v1.php?startTest",
                    success: function(data) {
                        appendDivWithScript(data);
                    }
                });
            } else {
                addNotification("Ошибка работы", "Сначала сделайте транскрибацию и конспект!", "Danger");
            }
        });
    });
}

function getAudioDuration(filePath) {
    return new Promise((resolve, reject) => {
        let audio = new Audio();
        audio.src = filePath;

        audio.onloadedmetadata = () => {
            resolve(audio.duration);
        };

        audio.onerror = () => {
            reject("Не удалось загрузить аудиофайл.");
        };
    });
}

function renderTranscribingBlock(transcribingText) {
    getFullInformationForInitialRender().then((data) => {
        getAudioDuration('/temp/' + data["audio_name"]).then(duration => {
            let audioDuration = duration;
            let time = parseFloat(audioDuration / 6.6).toFixed(2);

            if (data["status"] == "Transcribing") {
                let htmlObject = `<div class="bg-[#f1f3f4] rounded-[8px] justify-center flex items-center h-[200px] animate-pulse">
                    <div class="grid justify-center items-center justify-items-center">
                        <div class="mb-2">
                            <p class="text-[16px] font-medium text-[#b8b8b8]">Выполняется процесс транскрибации</p>
                            <p class="text-[14px] font-medium text-[#b8b8b8]">Примерное время выполнения ${time} секунд...</p>
                        </div>
                        <div>
                            <svg class="animate-spin text-[#b8b8b8] w-12 h-12" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M10.343 3.94c.09-.542.56-.94 1.11-.94h1.093c.55 0 1.02.398 1.11.94l.149.894c.07.424.384.764.78.93.398.164.855.142 1.205-.108l.737-.527a1.125 1.125 0 011.45.12l.773.774c.39.389.44 1.002.12 1.45l-.527.737c-.25.35-.272.806-.107 1.204.165.397.505.71.93.78l.893.15c.543.09.94.56.94 1.109v1.094c0 .55-.397 1.02-.94 1.11l-.893.149c-.425.07-.765.383-.93.78-.165.398-.143.854.107 1.204l.527.738c.32.447.269 1.06-.12 1.45l-.774.773a1.125 1.125 0 01-1.449.12l-.738-.527c-.35-.25-.806-.272-1.203-.107-.397.165-.71.505-.781.929l-.149.894c-.09.542-.56.94-1.11.94h-1.094c-.55 0-1.019-.398-1.11-.94l-.148-.894c-.071-.424-.384-.764-.781-.93-.398-.164-.854-.142-1.204.108l-.738.527c-.447.32-1.06.269-1.45-.12l-.773-.774a1.125 1.125 0 01-.12-1.45l.527-.737c.25-.35.273-.806.108-1.204-.165-.397-.505-.71-.93-.78l-.894-.15c-.542-.09-.94-.56-.94-1.109v-1.094c0-.55.398-1.02.94-1.11l.894-.149c.424-.07.765-.383.93-.78.165-.398.143-.854-.107-1.204l-.527-.738a1.125 1.125 0 01.12-1.45l.773-.773a1.125 1.125 0 011.45-.12l.737.527c.35.25.807.272 1.204.107.397-.165.71-.505.78-.929l.15-.894z"></path>
                                <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                            </svg>
                        </div>
                    </div>
                </div>`;
                $(".transcribing-block").html(htmlObject);
            } else if (transcribingText != null) {
                let htmlObject = `<div class="mb-2">
                    <textarea class="font-onest text-[15px] text-[#50667b] bg-[#ebedf7] rounded-[3px] px-[16px] py-[8px] outline-none focus:opacity-80 transition-all w-full transcribing-textarea" rows="20">${transcribingText}</textarea>
                </div>
                <div>
                    <button type="button" class="h-[40px] py-[10px] px-[16px] text-[14px] w-full font-medium bg-[#8d46f640] hover:opacity-80 text-center rounded-[4px] font-onest text-[#9655f6] transition-all save-edits-transcribing disabled:opacity-70 disabled:cursor-not-allowed">Сохранить изменения</button>
                </div>`;
                $(".transcribing-block").html(htmlObject);
            }
        }).catch(error => {
            console.error(error);
        });
    });
}


function renderSummaryBlock(summaryText, fileName) {

    getFullInformationForInitialRender().then((data) => {
        if (data["status"] == "Summarizing") {
            let htmlObject = `<div class="bg-[#f1f3f4] rounded-[8px] justify-center flex items-center h-[200px] animate-pulse">
                <div class="grid justify-center items-center justify-items-center">
                    <div class="mb-2">
                        <span class="text-[16px] font-medium text-[#b8b8b8]">Выполняется процесс составления конспекта</span>
                        <span class="text-[14px] font-medium text-[#b8b8b8]">Пожалуйста, подождите. Процесс занимает некоторое время...</span>
                    </div>
                    <div>
                        <svg class="animate-spin text-[#b8b8b8] w-12 h-12" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M10.343 3.94c.09-.542.56-.94 1.11-.94h1.093c.55 0 1.02.398 1.11.94l.149.894c.07.424.384.764.78.93.398.164.855.142 1.205-.108l.737-.527a1.125 1.125 0 011.45.12l.773.774c.39.389.44 1.002.12 1.45l-.527.737c-.25.35-.272.806-.107 1.204.165.397.505.71.93.78l.893.15c.543.09.94.56.94 1.109v1.094c0 .55-.397 1.02-.94 1.11l-.893.149c-.425.07-.765.383-.93.78-.165.398-.143.854.107 1.204l.527.738c.32.447.269 1.06-.12 1.45l-.774.773a1.125 1.125 0 01-1.449.12l-.738-.527c-.35-.25-.806-.272-1.203-.107-.397.165-.71.505-.781.929l-.149.894c-.09.542-.56.94-1.11.94h-1.094c-.55 0-1.019-.398-1.11-.94l-.148-.894c-.071-.424-.384-.764-.781-.93-.398-.164-.854-.142-1.204.108l-.738.527c-.447.32-1.06.269-1.45-.12l-.773-.774a1.125 1.125 0 01-.12-1.45l.527-.737c.25-.35.273-.806.108-1.204-.165-.397-.505-.71-.93-.78l-.894-.15c-.542-.09-.94-.56-.94-1.109v-1.094c0-.55.398-1.02.94-1.11l.894-.149c.424-.07.765-.383.93-.78.165-.398.143-.854-.107-1.204l-.527-.738a1.125 1.125 0 01.12-1.45l.773-.773a1.125 1.125 0 011.45-.12l.737.527c.35.25.807.272 1.204.107.397-.165.71-.505.78-.929l.15-.894z"></path>
                            <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                        </svg>
                    </div>
                </div>
            </div>`;
            $(".summary-block").html(htmlObject);
        } else if(summaryText != null) {
            let htmlObject = `<div class="mb-2">
                <textarea class="font-onest text-[15px] text-[#50667b] bg-[#ebedf7] rounded-[3px] px-[16px] py-[8px] outline-none focus:opacity-80 transition-all w-full summary-textarea" rows="20">${summaryText}</textarea>
            </div>
            <div class="flex gap-[6px]">
                <button type="button" class="h-[40px] py-[10px] px-[16px] text-[14px] w-full font-medium bg-green-100 hover:opacity-80 text-center rounded-[4px] font-onest text-green-700 transition-all download-summary disabled:opacity-70 disabled:cursor-not-allowed" file-name="${fileName}">Скачать .docx</button>
                <button type="button" class="h-[40px] py-[10px] px-[16px] text-[14px] w-full font-medium bg-[#8d46f640] hover:opacity-80 text-center rounded-[4px] font-onest text-[#9655f6] transition-all save-edits-summary disabled:opacity-70 disabled:cursor-not-allowed">Сохранить изменения</button>
            </div>`
    
            $(".summary-block").html(htmlObject);
        }
    });

    
    
}

function renderGlossaryBlock(glossaryText) {

        getFullInformationForInitialRender().then((data) => {
            if (data["status"] == "Glossary") {
                let htmlObject = `<div class="bg-[#f1f3f4] rounded-[8px] justify-center flex items-center h-[200px] animate-pulse">
                    <div class="grid justify-center items-center justify-items-center">
                        <div class="mb-2">
                            <span class="text-[16px] font-medium text-[#b8b8b8]">Выполняется процесс составления глоссария</span>
                            <span class="text-[14px] font-medium text-[#b8b8b8]">Пожалуйста, подождите. Процесс занимает некоторое время...</span>
                        </div>
                        <div>
                            <svg class="animate-spin text-[#b8b8b8] w-12 h-12" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M10.343 3.94c.09-.542.56-.94 1.11-.94h1.093c.55 0 1.02.398 1.11.94l.149.894c.07.424.384.764.78.93.398.164.855.142 1.205-.108l.737-.527a1.125 1.125 0 011.45.12l.773.774c.39.389.44 1.002.12 1.45l-.527.737c-.25.35-.272.806-.107 1.204.165.397.505.71.93.78l.893.15c.543.09.94.56.94 1.109v1.094c0 .55-.397 1.02-.94 1.11l-.893.149c-.425.07-.765.383-.93.78-.165.398-.143.854.107 1.204l.527.738c.32.447.269 1.06-.12 1.45l-.774.773a1.125 1.125 0 01-1.449.12l-.738-.527c-.35-.25-.806-.272-1.203-.107-.397.165-.71.505-.781.929l-.149.894c-.09.542-.56.94-1.11.94h-1.094c-.55 0-1.019-.398-1.11-.94l-.148-.894c-.071-.424-.384-.764-.781-.93-.398-.164-.854-.142-1.204.108l-.738.527c-.447.32-1.06.269-1.45-.12l-.773-.774a1.125 1.125 0 01-.12-1.45l.527-.737c.25-.35.273-.806.108-1.204-.165-.397-.505-.71-.93-.78l-.894-.15c-.542-.09-.94-.56-.94-1.109v-1.094c0-.55.398-1.02.94-1.11l.894-.149c.424-.07.765-.383.93-.78.165-.398.143-.854-.107-1.204l-.527-.738a1.125 1.125 0 01.12-1.45l.773-.773a1.125 1.125 0 011.45-.12l.737.527c.35.25.807.272 1.204.107.397-.165.71-.505.78-.929l.15-.894z"></path>
                                <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                            </svg>
                        </div>
                    </div>
                </div>`;
                $(".glossary-block").html(htmlObject);
                return;
        }

        if (glossaryText) {
            let glossaryArray;
            try {
                glossaryArray = JSON.parse(glossaryText);
            } catch (e) {
                console.error('Ошибка при парсинге glossaryText:', e);
                return;
            }
    
            let tableRows = glossaryArray.map(item => {
                let term = item.name.split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
                let definition = item.definition;
                let time = item.time;
    
                return `<tr class="even:bg-gray-50">
                            <td class="py-4 pl-4 pr-3 text-sm font-medium text-gray-900 sm:pl-3">${term}</td>
                            <td class="px-3 py-4 text-sm text-gray-500">${definition}</td>
                            <td class="px-3 py-4 text-sm text-gray-500">${time}</td>
                        </tr>`;
            }).join('');
    
            let tableHtml = `<div class="flow-root">
                                <div class="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
                                    <div class="inline-block py-2 align-middle sm:px-6 lg:px-8">
                                        <table class="divide-y divide-gray-300">
                                            <thead>
                                                <tr>
                                                    <th scope="col" class="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-3">Термин</th>
                                                    <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Определение</th>
                                                    <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Таймкод</th>
                                                </tr>
                                            </thead>
                                            <tbody class="bg-white">${tableRows}</tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>`;
    
            $(".glossary-block").html(tableHtml);
        }
    });

    
}

function renderTestBlock(testText) {

    getFullInformationForInitialRender().then((data) => {
            if (data["status"] == "Testing") {
                let htmlObject = `<div class="bg-[#f1f3f4] rounded-[8px] justify-center flex items-center h-[200px] animate-pulse">
                    <div class="grid justify-center items-center justify-items-center">
                        <div class="mb-2">
                            <span class="text-[16px] font-medium text-[#b8b8b8]">Выполняется процесс составления теста</span>
                            <span class="text-[14px] font-medium text-[#b8b8b8]">Пожалуйста, подождите. Процесс занимает некоторое время...</span>
                        </div>
                        <div>
                            <svg class="animate-spin text-[#b8b8b8] w-12 h-12" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M10.343 3.94c.09-.542.56-.94 1.11-.94h1.093c.55 0 1.02.398 1.11.94l.149.894c.07.424.384.764.78.93.398.164.855.142 1.205-.108l.737-.527a1.125 1.125 0 011.45.12l.773.774c.39.389.44 1.002.12 1.45l-.527.737c-.25.35-.272.806-.107 1.204.165.397.505.71.93.78l.893.15c.543.09.94.56.94 1.109v1.094c0 .55-.397 1.02-.94 1.11l-.893.149c-.425.07-.765.383-.93.78-.165.398-.143.854.107 1.204l.527.738c.32.447.269 1.06-.12 1.45l-.774.773a1.125 1.125 0 01-1.449.12l-.738-.527c-.35-.25-.806-.272-1.203-.107-.397.165-.71.505-.781.929l-.149.894c-.09.542-.56.94-1.11.94h-1.094c-.55 0-1.019-.398-1.11-.94l-.148-.894c-.071-.424-.384-.764-.781-.93-.398-.164-.854-.142-1.204.108l-.738.527c-.447.32-1.06.269-1.45-.12l-.773-.774a1.125 1.125 0 01-.12-1.45l.527-.737c.25-.35.273-.806.108-1.204-.165-.397-.505-.71-.93-.78l-.894-.15c-.542-.09-.94-.56-.94-1.109v-1.094c0-.55.398-1.02.94-1.11l.894-.149c.424-.07.765-.383.93-.78.165-.398.143-.854-.107-1.204l-.527-.738a1.125 1.125 0 01.12-1.45l.773-.773a1.125 1.125 0 011.45-.12l.737.527c.35.25.807.272 1.204.107.397-.165.71-.505.78-.929l.15-.894z"></path>
                                <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                            </svg>
                        </div>
                    </div>
                </div>`;
                $(".test-block").html(htmlObject);
                return;
        }
        if (testText) {
            let testArray;
            try {
                testArray = JSON.parse(testText);
            } catch (e) {
                console.error('Ошибка при парсинге testText:', e);
                return;
            }

            let htmlObject = testArray.map((item, index) => `
                <div class="mb-6">
                    <p class="font-onest font-normal text-[16px] text-[#191816] mb-2">${index + 1}. ${item.question}</p>
                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <span class="${item.answer === 'variant1' ? 'font-onest font-semibold text-[14px] text-green-500' : 'font-onest font-normal text-[14px] text-[#191816]'}">(A) ${item.variant1}</span>
                        </div>
                        <div>
                            <span class="${item.answer === 'variant2' ? 'font-onest font-semibold text-[14px] text-green-500' : 'font-onest font-normal text-[14px] text-[#191816]'}">(B) ${item.variant2}</span>
                        </div>
                        <div>
                            <span class="${item.answer === 'variant3' ? 'font-onest font-semibold text-[14px] text-green-500' : 'font-onest font-normal text-[14px] text-[#191816]'}">(C) ${item.variant3}</span>
                        </div>
                        <div>
                            <span class="${item.answer === 'variant4' ? 'font-onest font-semibold text-[14px] text-green-500' : 'font-onest font-normal text-[14px] text-[#191816]'}">(D) ${item.variant4}</span>
                        </div>
                    </div>
                </div>
            `).join('');

            htmlObject += `
                <div>
                    <button type="button" class="h-[40px] py-[10px] px-[16px] text-[14px] w-full font-medium bg-green-100 hover:opacity-80 text-center rounded-[4px] font-onest text-green-700 transition-all download-test disabled:opacity-70 disabled:cursor-not-allowed">Скачать автоматическое тестирование</button>
                </div>`;

            $(".test-block").html(htmlObject);
        }
}   );
}



function generateTestHtml(jsonString) {
    let jsonData;
    try {
        jsonData = JSON.parse(jsonString);
    } catch (e) {
        console.error('Ошибка при парсинге jsonData:', e);
        return '';
    }

    let htmlContent = `
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Автоматическое тестирование</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
        <script>
            function validateTest() {
                let correctAnswers = 0;
                const answers = ${JSON.stringify(jsonData.map(item => item.answer))};
                answers.forEach((answer, index) => {
                    if (document.querySelector(\`input[name="question\${index}"]:checked\`).value === answer) {
                        correctAnswers++;
                    }
                });
            
                let icon;
                let title;
                if (correctAnswers < 5) {
                    icon = 'error';
                    title = 'Попробуйте еще раз!';
                } else if (correctAnswers < 7) {
                    icon = 'warning';
                    title = 'Неплохо, но можно лучше!';
                } else {
                    icon = 'success';
                    title = 'Отлично!';
                }
            
                Swal.fire({
                    title: title,
                    text: \`Количество правильных ответов: \${correctAnswers} из \${answers.length}\`,
                    icon: icon,
                    confirmButtonText: 'Закрыть'
                });
            }        
        </script>
    </head>
    <body class="bg-[#f4f5fa]">
        <div class="container mx-auto p-4">
            <div class="bg-white p-[32px] rounded-[32px] mb-8">
                <div class="mb-4">
                    <h1 class="font-onest font-medium md:text-[24px] text-[20px] text-[#191816]">Тест</h1>
                </div>
                <div class="test-block">`;

    jsonData.forEach((item, index) => {
        htmlContent += `
            <div class="mb-6">
                <p class="font-onest font-normal text-[16px] text-[#191816] mb-2">${index + 1}. ${item.question}</p>
                <div class="grid grid-cols-2 gap-4">`;

        for (let i = 1; i <= 4; i++) {
            let variantKey = "variant" + i;
            htmlContent += `
                <div>
                    <label class="font-onest font-normal text-[14px] text-[#191816]">
                        <input type="radio" name="question${index}" value="variant${i}"> 
                        (${String.fromCharCode(65 + i - 1)}) ${item[variantKey]}
                    </label>
                </div>`;
        }

        htmlContent += `
                </div>
            </div>`;
    });

    htmlContent += `
                <div>
                    <button type="button" class="h-[40px] py-[10px] px-[16px] text-[14px] font-medium bg-[#8d46f640] hover:opacity-80 text-center rounded-[4px] font-onest text-[#9655f6] transition-all" onclick="validateTest()">Проверить ответы</button>
                </div>
            </div>
        </div>
    </body>
    </html>`;

    return htmlContent;
}

function downloadTest(jsonData) {
    const testHtml = generateTestHtml(jsonData);
    const blob = new Blob([testHtml], { type: 'text/html' });
    const href = URL.createObjectURL(blob);

    const downloadLink = document.createElement('a');
    downloadLink.href = href;
    downloadLink.download = 'test.html';
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
    URL.revokeObjectURL(href);
}

function rerenderAllInformation() {
    appendTitle(lastData["lecture_name"]);
    appendAudio(lastData["audio_name"]);
    appendSteps(lastData["text_transcription"], lastData["text_summary"], lastData["text_glossary"], lastData["text_test"]);

    renderTranscribingBlock(lastData["text_transcription"]);
    renderSummaryBlock(lastData["text_summary"], lastData["filename_summary"]);
    renderGlossaryBlock(lastData["text_glossary"]);
    renderTestBlock(lastData["text_test"]);
}

setInterval(checkForUpdates, 10000);