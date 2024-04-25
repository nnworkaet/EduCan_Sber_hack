<?php

include_once __DIR__ . '/../Custom/Medoo/connect.php';
include_once __DIR__ . '/../Functions/utility.class.php';

@session_start();

$utilityClass = new UtilityClass();

// http://server:8080/
$apiUrl = "YOUR_URL_HERE";

if(isset($_GET['authUser'])) {

    if(!empty($_POST['login']) && !empty($_POST['password'])) {

        $login = $utilityClass->sanitizeParam($_POST['login']);
        $password = $utilityClass->sanitizeParam($_POST['password']);
    
        $databaseCallback = $database->get("gb_users", ["id", "login", "role"], ["login" => $login, "password" => md5($password)]);
    
        if (empty($databaseCallback['id'])) {
            $utilityClass->addJavaScript('addNotification("Ошибка авторизации", "Введенные данные неверны. Повторите попытку!", "Danger")');
            exit();
        }
    
        $_SESSION['id'] = $databaseCallback['id'];
        $_SESSION['login'] = $login;
        $_SESSION['role'] = $databaseCallback['role'];
    
        exit($utilityClass->changeLocationViaHTML('0', './dashboard'));

    }

}

if(isset($_GET["uploadNewAudio"])) {
    $utilityClass->checkSessions("dashboardAccess", $database);

    if(isset($_FILES['file']) && $_FILES['file']['error'] == 0) {
        $originalName = $_FILES['file']['name'];
        $extension = pathinfo($originalName, PATHINFO_EXTENSION);
        $randomName = rand(1000000000, 9999999999) . "." . $extension;
        $filePath = __DIR__ . "/../../temp/" . $randomName;

        if(move_uploaded_file($_FILES['file']['tmp_name'], $filePath)) {
            $lectureName = isset($_POST['lectureName']) ? $utilityClass->sanitizeParam($_POST['lectureName']) : '';

            $fileWeight = round(filesize($filePath) / 1024 / 1024, 4);

            $database->insert('gb_audio', [
                'audio_name' => $randomName,
                'lecture_name' => $lectureName,
                'status' => 'Uploaded',
                'file_weight' => $fileWeight,
                'user_id' => $utilityClass->id(),
                'updated_at' => $utilityClass->getCurrentDateTime()
            ]);

            $utilityClass->addJavaScript('addNotification("Успех", "Файл успешно загружен!", "Success")');

            exit($utilityClass->changeLocationViaHTML('1500', './results'));

        } else {
            $utilityClass->addJavaScript('addNotification("Ошибка загрузки файла", "Невозможно переместить данный файл в каталог!", "Danger")');
        }
    } else {
        $utilityClass->addJavaScript('addNotification("Ошибка загрузки файла", "Загрузите как минимум 1 аудио файл!", "Danger")');
    }

    exit($utilityClass->changeLocationViaHTML('1500', './dashboard'));

}

if(isset($_GET['getInformationForInitialRender'])) {

    $utilityClass->checkSessions("dashboardAccess", $database);

    $databaseCallback = $database->select("gb_audio", ["id", "lecture_name", "status", "updated_at"], ["ORDER" => [
        "id" => "DESC"
    ], "user_id" => $utilityClass->id()]);

    foreach ($databaseCallback as $databaseQuery) {
        $output[] = [
            'identity' => $databaseQuery['id'],
            'lectureName' => $databaseQuery['lecture_name'],
            'status' => $databaseQuery['status'],
            'updatedAt' => $databaseQuery['updated_at']
        ];
    }

    header('Content-Type: application/json');
    echo json_encode($output, JSON_UNESCAPED_UNICODE);
    
}

if(isset($_GET['getAdminInformationForInitialRender'])) {

    $utilityClass->checkSessions("dashboardAccess", $database);
    $utilityClass->checkSessions("adminAccess", $database);

    $databaseCallback = $database->select("gb_audio", ["id", "lecture_name", "status", "user_id", "updated_at"], ["ORDER" => [
        "id" => "DESC"
    ]]);

    foreach ($databaseCallback as $databaseQuery) {

        $databaseUserName = $database->get("gb_users", "login", [
            "id" => $databaseQuery['user_id']
        ]);

        $output[] = [
            'identity' => $databaseQuery['id'],
            'lectureName' => $databaseQuery['lecture_name'],
            'status' => $databaseQuery['status'],
            'login' => $databaseUserName,
            'updatedAt' => $databaseQuery['updated_at']
        ];
    }

    header('Content-Type: application/json');
    echo json_encode($output, JSON_UNESCAPED_UNICODE);
    
}

if(isset($_GET['getFullInformationForInitialRender'])) {

    $utilityClass->checkSessions("dashboardAccess", $database);

    if(!empty($_POST['identity'])) {

        $databaseCallback = $database->get("gb_audio", ["id", "audio_name", "lecture_name", "status", "text_transcription", "text_glossary", "text_summary", "filename_summary", "text_test", "file_weight", "updated_at"], [
            "id" => $_POST["identity"]
        ]);
    
        header('Content-Type: application/json');
        echo json_encode($databaseCallback, JSON_UNESCAPED_UNICODE);

    }
    
}

if(isset($_GET['startTranscription'])) {
    $utilityClass->checkSessions("dashboardAccess", $database);

    if(!empty($_POST['identity'])) {

        $databaseCallback = $database->update("gb_audio", [
            "status" => "Transcribing", 
            "updated_at" => $utilityClass->getCurrentDateTime()
        ], [
            "id" => $_POST["identity"]
        ]);

        $databaseAudioName = $database->get("gb_audio", "audio_name", [
            "id" => $_POST["identity"]
        ]);

        $audioPath = $utilityClass->getFullServerUrl() . "/temp/" . $databaseAudioName;

        $jsonData = json_encode([
            'identity' => $_POST["identity"],
            'audioPath' => $audioPath
        ]);

        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $apiUrl . "requestTranscription");
        curl_setopt($ch, CURLOPT_POST, 1);

        curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));

        curl_setopt($ch, CURLOPT_POSTFIELDS, $jsonData);

        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

        $response = curl_exec($ch);
        curl_close($ch);
    
        exit($utilityClass->addJavaScript('addNotification("Успех", "Ваш запрос отправлен на обработку!", "Success")'));

    }
}

if(isset($_GET['startSummary'])) {
    $utilityClass->checkSessions("dashboardAccess", $database);

    if(!empty($_POST['identity'])) {

        $databaseCallback = $database->update("gb_audio", [
            "status" => "Summarizing", 
            "updated_at" => $utilityClass->getCurrentDateTime()
        ], [
            "id" => $_POST["identity"]
        ]);

        $databaseTextTime = $database->get("gb_audio", "text_transcription_time", [
            "id" => $_POST["identity"]
        ]);

        $jsonData = json_encode([
            'identity' => $_POST["identity"],
            'txt' => $databaseTextTime
        ]);

        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $apiUrl . "requestSum");
        curl_setopt($ch, CURLOPT_POST, 1);

        curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));

        curl_setopt($ch, CURLOPT_POSTFIELDS, $jsonData);

        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

        $response = curl_exec($ch);
        curl_close($ch);
    
        exit($utilityClass->addJavaScript('addNotification("Успех", "Ваш запрос отправлен на обработку!", "Success")'));

    }
}

if(isset($_GET['startGlossary'])) {
    $utilityClass->checkSessions("dashboardAccess", $database);

    if(!empty($_POST['identity'])) {

        $databaseCallback = $database->update("gb_audio", [
            "status" => "Glossary", 
            "updated_at" => $utilityClass->getCurrentDateTime()
        ], [
            "id" => $_POST["identity"]
        ]);

        $databaseTextTime = $database->get("gb_audio", "text_transcription_time", [
            "id" => $_POST["identity"]
        ]);

        $jsonData = json_encode([
            'identity' => $_POST["identity"],
            'txt' => $databaseTextTime
        ]);

        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $apiUrl . "requestTermins");
        curl_setopt($ch, CURLOPT_POST, 1);

        curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));

        curl_setopt($ch, CURLOPT_POSTFIELDS, $jsonData);

        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

        $response = curl_exec($ch);
        curl_close($ch);
    
        exit($utilityClass->addJavaScript('addNotification("Успех", "Ваш запрос отправлен на обработку!", "Success")'));

    }
}

if(isset($_GET['startTest'])) {
    $utilityClass->checkSessions("dashboardAccess", $database);

    if(!empty($_POST['identity'])) {

        $databaseCallback = $database->update("gb_audio", [
            "status" => "Testing", 
            "updated_at" => $utilityClass->getCurrentDateTime()
        ], [
            "id" => $_POST["identity"]
        ]);

        $databaseTextTime = $database->get("gb_audio", "text_transcription_time", [
            "id" => $_POST["identity"]
        ]);

        $jsonData = json_encode([
            'identity' => $_POST["identity"],
            'txt' => $databaseTextTime
        ]);

        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $apiUrl . "requestTest");
        curl_setopt($ch, CURLOPT_POST, 1);

        curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));

        curl_setopt($ch, CURLOPT_POSTFIELDS, $jsonData);

        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

        $response = curl_exec($ch);
        curl_close($ch);
    
        exit($utilityClass->addJavaScript('addNotification("Успех", "Ваш запрос отправлен на обработку!", "Success")'));

    }
}

if(isset($_GET['saveEditsTranscribing'])) {
    $utilityClass->checkSessions("dashboardAccess", $database);

    if(!empty($_POST['identity']) && !empty($_POST['textTranscription'])) {

        $databaseCallback = $database->update("gb_audio", [
            "text_transcription" => $_POST['textTranscription'],
            "updated_at" => $utilityClass->getCurrentDateTime()
        ], [
            "id" => $_POST["identity"]
        ]);
    
        exit($utilityClass->addJavaScript('addNotification("Успех", "Изменения сохранены!", "Success")'));

    }
}


if(isset($_GET['saveEditsSummary'])) {
    $utilityClass->checkSessions("dashboardAccess", $database);

    if(!empty($_POST['identity']) && !empty($_POST['textSummary'])) {

        $databaseCallback = $database->update("gb_audio", [
            "text_summary" => $_POST['textSummary'],
            "updated_at" => $utilityClass->getCurrentDateTime()
        ], [
            "id" => $_POST["identity"]
        ]);
    
        exit($utilityClass->addJavaScript('addNotification("Успех", "Изменения сохранены!", "Success")'));

    }
}

if(isset($_GET['saveNewPassword'])) {

    $utilityClass->checkSessions("dashboardAccess", $database);

    $oldPassword = $utilityClass->sanitizeParam($_POST['oldPassword']);
    $newPassword = $utilityClass->sanitizeParam($_POST['newPassword']);

    $databasePassword = $database->get("gb_users", "password", ["id" => $_SESSION["id"]]);

    if($databasePassword != md5($oldPassword)) {
        $utilityClass->addJavaScript('addNotification("Ошибка сохранения", "Старый пароль не совпадает с введенным, повторите попытку!", "Danger")');
        exit();
    }

    $databaseCallback = $database->update("gb_users", [
        "password" => md5($newPassword)
    ], ["id" => $_SESSION["id"]]);

    $response = [
        "response" => "success"
    ];

    echo json_encode($response);
  
}

if(isset($_GET['getAllUsers'])) {

    $utilityClass->checkSessions("dashboardAccess", $database);
    $utilityClass->checkSessions("adminAccess", $database);

    $databaseCallback = $database->select("gb_users", ["id", "login", "role"], ["ORDER" => [
        "id" => "DESC",
    ]]);

    foreach ($databaseCallback as $databaseQuery) {
        $output[] = [
            'identity' => (string) $databaseQuery['id'],
            'login' => $databaseQuery['login'],
            'role' => $databaseQuery['role'],
        ];
    }

    header('Content-Type: application/json');
    echo json_encode($output);
    
}


if(isset($_GET['deleteUser'])) {

    $utilityClass->checkSessions("dashboardAccess", $database);
    $utilityClass->checkSessions("adminAccess", $database);

    $userId = $utilityClass->sanitizeParam($_POST['userId']);

    $databaseLogin = $database->delete("gb_users", ["id" => $userId]);

    $response = [
        "response" => "success"
    ];

    echo json_encode($response);
  
}

if(isset($_GET['createNewUser'])) {

    $utilityClass->checkSessions("dashboardAccess", $database);
    $utilityClass->checkSessions("adminAccess", $database);

    $login = $utilityClass->sanitizeParam($_POST['login']);
    $role = $utilityClass->sanitizeParam($_POST['role']);
    $password = $utilityClass->sanitizeParam($_POST['password']);

    $databaseLogin = $database->has("gb_users", ["login" => $login]);

    if($databaseLogin) {
        $utilityClass->addJavaScript('addNotification("Ошибка регистрации", "Пользователь с таким логином уже существует!", "Danger")');
        exit();
    }

    $databaseCallback = $database->insert("gb_users", [
        "login" => $login,
        "password" => md5($password),
        "role" => $role
    ]);

    $response = [
        "response" => "success"
    ];

    echo json_encode($response);
  
}

if(isset($_GET['appendTranscriptionText'])) {

    $identity = $utilityClass->sanitizeParam($_POST['identity']);
    $text = $_POST['text'];
    $textTime = $_POST['textTime'];

    if(!empty($identity) && !empty($text)) {
        $databaseCallback = $database->update("gb_audio", [
            "text_transcription" => $text,
            "text_transcription_time" => $textTime,
            "status" => "All Done",
            "updated_at" => $utilityClass->getCurrentDateTime()
        ], ["id" => $identity]);
    
        $response = [
            "response" => "success"
        ];
    
        echo json_encode($response);

        return;
    } 

    $response = [
        "response" => "error"
    ];

    echo json_encode($response);
  
}

if(isset($_GET['appendSummary'])) {

    if(isset($_FILES['file']) && $_FILES['file']['error'] == 0) {

        $identity = $utilityClass->sanitizeParam($_POST['identity']);
        $text = $_POST['text'];

        $originalName = $_FILES['file']['name'];
        $extension = pathinfo($originalName, PATHINFO_EXTENSION);
        $randomName = rand(1000000000, 9999999999) . "." . $extension;
        $filePath = __DIR__ . "/../../temp/" . $randomName;

        if(move_uploaded_file($_FILES['file']['tmp_name'], $filePath)) {

            $databaseCallback = $database->update("gb_audio", [
                "text_summary" => $text,
                "filename_summary" => $randomName,
                "status" => "All Done","status" => "All Done",
                "updated_at" => $utilityClass->getCurrentDateTime()
            ], ["id" => $identity]);

            $response = [
                "response" => "success"
            ];
        
            echo json_encode($response);

        } else {
            $response = [
                "response" => "error1"
            ];
        
            echo json_encode($response);
        }
    } else {
        $response = [
            "response" => "error2"
        ];
    
        echo json_encode($response);
    }
  
}

if(isset($_GET['appendGlossaryText'])) {

    $identity = $utilityClass->sanitizeParam($_POST['identity']);
    $text = $_POST['text'];

    if(!empty($identity) && !empty($text)) {
        $databaseCallback = $database->update("gb_audio", [
            "text_glossary" => $text,
            "status" => "All Done",
            "updated_at" => $utilityClass->getCurrentDateTime()
        ], ["id" => $identity]);
    
        $response = [
            "response" => "success"
        ];
    
        echo json_encode($response);
    } 
  
}

if(isset($_GET['appendTestText'])) {

    $identity = $utilityClass->sanitizeParam($_POST['identity']);
    $text = $_POST['text'];

    if(!empty($identity) && !empty($text)) {
        $databaseCallback = $database->update("gb_audio", [
            "text_test" => $text,
            "status" => "All Done",
            "updated_at" => $utilityClass->getCurrentDateTime()
        ], ["id" => $identity]);
    
        $response = [
            "response" => "success"
        ];
    
        echo json_encode($response);
    } 
  
}