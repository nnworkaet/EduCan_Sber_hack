$(document).on('click', '.open-audio', function() {
    var audioId = $(this).attr('audio-id');
    if (audioId) {
        localStorage.setItem('selectedAudioId', audioId);
        window.location.href = '/log';
    } else {
        console.error('Audio ID не найден');
    }
});


function getInitialAudioInformation() {
    return new Promise((resolve, reject) => {
        $.ajax({
            type: "GET",
            url: "./src/Api/v1.php?getAdminInformationForInitialRender",
            success: function(data) {
                resolve(data);
            },
            error: function(error) {
                reject(error);
            }
        });
    });
}

function createAudioListHtml() {
    return getInitialAudioInformation().then(data => {
        let ulHtml = '<ul role="list" class="divide-y divide-gray-100 w-full">';

        data.forEach(item => {

            if(item.status == "Uploaded") {
                badge = `<p class="rounded-md whitespace-nowrap mt-0.5 px-1.5 py-0.5 text-xs font-medium ring-1 ring-inset text-green-700 bg-green-50 ring-green-600/20 font-onest">Загружено</p>`;
            } else if(item.status == "Transcribing") {
                badge = `<p class="rounded-md whitespace-nowrap mt-0.5 px-1.5 py-0.5 text-xs font-medium ring-1 ring-inset text-amber-700 bg-amber-50 ring-amber-600/20 font-onest">Транскрибация</p>`;
            } else if(item.status == "Testing") {
                badge = `<p class="rounded-md whitespace-nowrap mt-0.5 px-1.5 py-0.5 text-xs font-medium ring-1 ring-inset text-blue-700 bg-blue-50 ring-blue-600/20 font-onest">Тестирование</p>`;
            } else if(item.status == "Glossary") {
                badge = `<p class="rounded-md whitespace-nowrap mt-0.5 px-1.5 py-0.5 text-xs font-medium ring-1 ring-inset text-indigo-700 bg-indigo-50 ring-indigo-600/20 font-onest">Составление Глоссария</p>`;
            } else if(item.status == "Summarizing") {
                badge = `<p class="rounded-md whitespace-nowrap mt-0.5 px-1.5 py-0.5 text-xs font-medium ring-1 ring-inset text-teal-700 bg-teal-50 ring-teal-600/20 font-onest">Суммаризация</p>`;
            } else if(item.status == "All Done") {
                badge = `<p class="rounded-md whitespace-nowrap mt-0.5 px-1.5 py-0.5 text-xs font-medium ring-1 ring-inset text-emerald-700 bg-emerald-50 ring-emerald-600/20 font-onest">Все Готово</p>`;
            }

            ulHtml += `
                <li class="md:flex grid items-center justify-between gap-x-6 py-5">
                    <div class="min-w-0 md:mb-0 mb-2">
                        <div class="flex items-start gap-x-3">
                            <p class="text-sm font-semibold leading-6 text-gray-900 font-onest">${item.lectureName}</p>
                            ${badge}
                            <p class="-ml-2 rounded-md whitespace-nowrap mt-0.5 px-1.5 py-0.5 text-xs font-medium ring-1 ring-inset text-purple-700 bg-purple-50 ring-purple-600/20 font-onest">${item.login}</p>
                        </div>
                        <div class="mt-1 flex items-center gap-x-2 text-xs leading-5 text-gray-500">
                            <p class="whitespace-nowrap font-onest">Изменение: <span>${item.updatedAt}</span></p>
                        </div>
                    </div>
                    <div class="flex flex-none items-center gap-x-4">
                        <button type="button" audio-id="${item.identity}" class="rounded-md bg-white px-2.5 py-1.5 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 block font-onest open-audio">Просмотреть</button>
                    </div>
                </li>
            `;
        });

        ulHtml += '</ul>';
        return ulHtml;
    }).catch(error => {
        console.error('Ошибка при получении данных: ', error);
        return '';
    });
}

createAudioListHtml().then(html => {
    $(".audio-render-div").html(html);
});