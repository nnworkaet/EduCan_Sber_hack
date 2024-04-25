<?php

class Templates
{
    public function documentHead($pageName) {
        ?>
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Обработчик текста | <?=$pageName;?></title>
            <link rel="icon" sizes="16x16" type="image/png" href="./public/img/favicon-16x16.png">
            <script src="https://cdn.tailwindcss.com"></script>
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Onest:wght@100;200;300;400;500;600;700;800;900&family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap" rel="stylesheet">
            <link rel="stylesheet" href="./public/css/gb.bundle.css">
            <?php
            switch ($pageName) {
                case 'Dashboard':
                    ?>
                    <link rel="stylesheet" href="./public/css/plugins/dropzone.min.css" type="text/css" />
                    <?
                    break;

                default:
                    ?> <?
                    break;
            }
            ?>
        </head>
        <?
    }

    public function documentJavascript($pageName) {
        ?>
        <script src="./public/js/plugins/jquery-3.7.1.min.js"></script>
        <script src="./public/js/main.js"></script>
        <?php

        switch ($pageName) {
            case 'Sign In':
                ?>
                <script src="./public/js/pages/sign-in.js"></script>
                <?
                break;

            case 'Dashboard':
                ?>
                <script src="./public/js/plugins/dropzone.min.js"></script>
                <script src="./public/js/pages/dashboard.js"></script>
                <?
                break;

            case 'Results':
                ?>
                <script src="./public/js/pages/results.js"></script>
                <?
                break;

            case 'Audio':
                ?>
                <script src="./public/js/pages/audio.js"></script>
                <?
                break;

            case 'Settings':
                ?>
                <script src="./public/js/pages/settings.js"></script>
                <?
                break;

            case 'Users':
                ?>
                <script src="./public/js/plugins/sweetalert.js"></script>
                <script src="./public/js/pages/users.js"></script>
                <?
                break;  
                
            case 'Logs':
                ?>
                <script src="./public/js/pages/logs.js"></script>
                <?
                break;

            case 'Log':
                ?>
                <script src="./public/js/pages/log.js"></script>
                <?
                break;

            default:
                ?> <?
                break;
        }
    }

    public function livepanelNavbar() {
        ?>
        <nav class="relative mx-auto w-full max-w-7xl px-4 lg:px-0">
            <div class="flex w-full flex-col items-center justify-between md:h-16 md:flex-row">
                <div class="w-full grow md:w-auto">
                    <div class="flex h-16 w-full items-center gap-x-4">
                        <div class="flex items-center justify-center">
                            <img src="./public/img/logo.png" class="w-10 h-10 mr-3">
                            <span class="text-[15px] font-medium text-[#0ea5e9d6]">Universal Livepanel Engine</span>
                        </div>
                    </div>
                </div>
            </div>
        </nav>
        <?php
    }

    public function geekBrainsNavigation($pageName) {

        $utilityClass = new UtilityClass();

        ?>
                        <div class="bg-white p-6 rounded-[32px] md:grid flex items-center md:justify-center justify-start gap-[16px] overflow-x-auto">
                            <a href="/dashboard" class="flex items-center gap-[12px] py-[12px] px-[16px] hover:bg-[#eff0f5] transition-all rounded-[8px] w-[188px] <?php if ($pageName == "Upload") {?>!bg-[#f4f5fa]<?php } ?>">
                                <div>
                                    <svg class="w-6 h-6 text-[#7c8092] <?php if ($pageName == "Upload") {?>!text-[#8d46f6]<?php } ?>" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 16.5V9.75m0 0l3 3m-3-3l-3 3M6.75 19.5a4.5 4.5 0 01-1.41-8.775 5.25 5.25 0 0110.233-2.33 3 3 0 013.758 3.848A3.752 3.752 0 0118 19.5H6.75z"></path>
                                    </svg>
                                </div>
                                <div>
                                    <span class="text-[#7c8092] font-onest font-medium text-[18px] <?php if ($pageName == "Upload") {?>!text-[#8d46f6]<?php } ?>">Загрузка</span>
                                </div>
                            </a>
                            <a href="/results" class="flex items-center gap-[12px] py-[12px] px-[16px] hover:bg-[#eff0f5] transition-all rounded-[8px] w-[188px] <?php if ($pageName == "Results") {?>!bg-[#f4f5fa]<?php } ?>">
                                <div>
                                    <svg class="w-6 h-6 text-[#7c8092] <?php if ($pageName == "Results") {?>!text-[#8d46f6]<?php } ?>" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z"></path>
                                    </svg>
                                </div>
                                <div>
                                    <span class="text-[#7c8092] font-onest font-medium text-[18px] <?php if ($pageName == "Results") {?>!text-[#8d46f6]<?php } ?>">Результаты</span>
                                </div>
                            </a>
                            <hr class="border">
                            <a href="/settings" class="flex items-center gap-[12px] py-[12px] px-[16px] hover:bg-[#eff0f5] transition-all rounded-[8px] w-[188px] <?php if ($pageName == "Settings") {?>!bg-[#f4f5fa]<?php } ?>">
                                <div>
                                    <svg class="w-6 h-6 text-[#7c8092] <?php if ($pageName == "Settings") {?>!text-[#8d46f6]<?php } ?>" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.324.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 011.37.49l1.296 2.247a1.125 1.125 0 01-.26 1.431l-1.003.827c-.293.24-.438.613-.431.992a6.759 6.759 0 010 .255c-.007.378.138.75.43.99l1.005.828c.424.35.534.954.26 1.43l-1.298 2.247a1.125 1.125 0 01-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.57 6.57 0 01-.22.128c-.331.183-.581.495-.644.869l-.213 1.28c-.09.543-.56.941-1.11.941h-2.594c-.55 0-1.02-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 01-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 01-1.369-.49l-1.297-2.247a1.125 1.125 0 01.26-1.431l1.004-.827c.292-.24.437-.613.43-.992a6.932 6.932 0 010-.255c.007-.378-.138-.75-.43-.99l-1.004-.828a1.125 1.125 0 01-.26-1.43l1.297-2.247a1.125 1.125 0 011.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.087.22-.128.332-.183.582-.495.644-.869l.214-1.281z"></path>
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                                    </svg>
                                </div>
                                <div>
                                    <span class="text-[#7c8092] font-onest font-medium text-[18px] <?php if ($pageName == "Settings") {?>!text-[#8d46f6]<?php } ?>">Настройки</span>
                                </div>
                            </a>
                            <?php
                            if($utilityClass->getUsersAccessType() == "admin") {
                            ?>
                            <hr class="border">
                            <a href="/users" class="flex items-center gap-[12px] py-[12px] px-[16px] hover:bg-[#eff0f5] transition-all rounded-[8px] w-[188px] <?php if ($pageName == "Users") {?>!bg-[#f4f5fa]<?php } ?>">
                                <div>
                                    <svg class="w-6 h-6 text-[#7c8092] <?php if ($pageName == "Users") {?>!text-[#8d46f6]<?php } ?>" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z"></path>
                                    </svg>
                                </div>
                                <div>
                                    <span class="text-[#7c8092] font-onest font-medium text-[18px] <?php if ($pageName == "Users") {?>!text-[#8d46f6]<?php } ?>">Пользователи</span>
                                </div>
                            </a>
                            <a href="/logs" class="flex items-center gap-[12px] py-[12px] px-[16px] hover:bg-[#eff0f5] transition-all rounded-[8px] w-[188px] <?php if ($pageName == "Logs") {?>!bg-[#f4f5fa]<?php } ?>">
                                <div>
                                    <svg class="w-6 h-6 text-[#7c8092] <?php if ($pageName == "Logs") {?>!text-[#8d46f6]<?php } ?>" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                                        <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25"></path>
                                    </svg>
                                </div>
                                <div>
                                    <span class="text-[#7c8092] font-onest font-medium text-[18px] <?php if ($pageName == "Logs") {?>!text-[#8d46f6]<?php } ?>">Журнал</span>
                                </div>
                            </a>
                            <?php
                            }
                            ?>
                        </div>
        <?php
    }
}

