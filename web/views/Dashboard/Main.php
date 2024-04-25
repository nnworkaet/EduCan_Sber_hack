<?php
$templates = new Templates();

$templates->documentHead("Dashboard");
?>
<body class="bg-[#f4f5fa]">
    <header class="bg-white mb-8">
        <div class="flex items-center justify-between md:px-20 px-8 py-6">
            <div>
                <img src="./public/img/geekbrains-logo-light.svg" class="w-[186px] h-[24px] cursor-pointer">
            </div>
            <div class="flex items-center">
                <div>
                    <a href="/logout" class="bg-[#e1e1e9] text-[#191816] text-[16px] py-[12px] px-[20px] rounded-[12px] font-onest font-medium hover:bg-[#d4d4dd] transition-all">Выход</a>
                </div>
            </div>
        </div>
    </header>
    <main>
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div class="mx-auto max-w-7xl">
                <div class="md:flex md:flex-grow md:gap-[24px]">
                    <div class="md:basis-3/12 md:mb-0 mb-6">
                        <?php $templates->geekBrainsNavigation("Upload"); ?>
                    </div>
                    <div class="md:basis-9/12">
                        <div class="bg-white p-[32px] rounded-[32px]">
                            <div class="mb-4">
                                <h1 class="font-onest font-medium md:text-[24px] text-[20px] text-[#191816]">Загрузка аудио файла</h1>
                            </div>
                            <div>
                                <div class="grid mb-6">
                                    <label class="font-onest text-[16px] text-[#191816] mb-1">Введите название для лекции:</label>
                                    <input type="text" class="font-onest text-[15px] text-[#50667b] bg-[#ebedf7] rounded-[3px] px-[16px] py-[8px] outline-none focus:opacity-80 transition-all w-full lecture-name-input" placeholder="Python для новичков. Основы алгоритмов, циклов и так далее...">
                                </div>

                                <div class="flex items-center justify-center w-full mb-6">
                                    <label for="dropzone-file" class="flex flex-col items-center justify-center w-full h-64 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100 dropzone-label">
                                        <div class="flex flex-col items-center justify-center pt-5 pb-6 dropzone-div">
                                            <svg class="w-10 h-10 mb-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>
                                            <p class="mb-2 text-sm text-gray-500 font-onest text-center md:p-0 p-2"><span class="font-semibold">Кликните для загрузки</span> или перенесите файл в зону</p>
                                            <p class="text-xs text-gray-500 font-onest">MP3, OGG или ДРУГОЕ АУДИО (МАКС. 100 мегабайт)</p>
                                        </div>
                                        <input id="dropzone-file" type="file" class="hidden" />
                                    </label>
                                </div>

                                <div>
                                    <button type="button" class="h-[40px] py-[10px] px-[16px] text-[14px] w-full font-medium bg-[#8d46f640] hover:opacity-80 text-center rounded-[4px] font-onest text-[#9655f6] transition-all upload-button disabled:opacity-70 disabled:cursor-not-allowed">Загрузить</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </main>
    <?php
    $templates->documentJavascript("Dashboard");
    ?>
</body>
</html>