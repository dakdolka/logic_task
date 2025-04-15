document.addEventListener('DOMContentLoaded', function () {
  // Получаем элементы кнопки и файлов
  const uploadButton = document.getElementById('uploadAllFiles');
  const fileInput1 = document.getElementById('file1');
  const fileInput2 = document.getElementById('file2');
  const selectFileButton1 = document.getElementById('selectFile1');
  const selectFileButton2 = document.getElementById('selectFile2');
  const fileNameDisplay1 = document.getElementById('fileName1');
  const fileNameDisplay2 = document.getElementById('fileName2');


  // Функция для обновления имени файла в плашечке
  function updateFileNameDisplay(inputElement, displayElement) {
    const file = inputElement.files[0];
    if (file) {
      displayElement.textContent = file.name;
    } else {
      displayElement.textContent = "Выберите файл";
    }
  }

  // Функция для отправки файлов
    function uploadFiles(file1, file2) {
      const formData = new FormData();
      formData.append('file1', file1);
      formData.append('file2', file2);

      fetch('http://192.168.71.128//api/upload', {
        method: 'POST',
        body: formData
      })
      .then(res => res.json())
      .then(data => {
        alert('Общий объем: ' + data.volume + 'л');  // Можешь изменить на alert или просто выполнить другие действия
      })
      .catch(err => {
        console.error(err);
        alert('Ошибка при загрузке');
      });
    }

  // Обработчик для кнопки отправки файлов
  uploadButton.addEventListener('click', function() {
    const file1 = fileInput1.files[0];  // Получаем файл 1
    const file2 = fileInput2.files[0];  // Получаем файл 2

    if (!file1 || !file2) {
      alert('Пожалуйста, выберите оба файла перед отправкой.');
      return;
    }

    // Отправляем оба файла на сервер
    uploadFiles(file1, file2);
  });

  // Обработчик для кнопки выбора файла 1
  selectFileButton1.addEventListener('click', function() {
    fileInput1.click();
  });

  // Обработчик для кнопки выбора файла 2
  selectFileButton2.addEventListener('click', function() {
    fileInput2.click();
  });

  // Обновление имени файла при изменении в input[type="file"]
  fileInput1.addEventListener('change', function() {
    updateFileNameDisplay(fileInput1, fileNameDisplay1);
  });

  fileInput2.addEventListener('change', function() {
    updateFileNameDisplay(fileInput2, fileNameDisplay2);
  });

  // Обработчики для дроп-зон

  // Функция для предотвращения стандартного поведения
  function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
  }

  // Добавляем обработчик dragover для обеих зон
  function handleDragOver(e) {
    preventDefaults(e);
    e.target.classList.add('dragover');
  }

  // Убираем стили при завершении перетаскивания
  function handleDragLeave(e) {
    preventDefaults(e);
    e.target.classList.remove('dragover');
  }

  // Обработчик для дроп-зоны
  function handleDrop(e, fileInput, fileNameDisplay) {
    preventDefaults(e);
    e.target.classList.remove('dragover');

    const file = e.dataTransfer.files[0];
    if (file) {
      // Добавляем файл в input и обновляем плашечку
      fileInput.files = e.dataTransfer.files;
      updateFileNameDisplay(fileInput, fileNameDisplay);
    }
  }

  // Добавляем обработчики для обеих зон
  const dropzone1 = document.getElementById('dropzone1');
  const dropzone2 = document.getElementById('dropzone2');

  dropzone1.addEventListener('dragover', handleDragOver);
  dropzone1.addEventListener('dragleave', handleDragLeave);
  dropzone1.addEventListener('drop', function(e) {
    handleDrop(e, fileInput1, fileNameDisplay1);
  });

  dropzone2.addEventListener('dragover', handleDragOver);
  dropzone2.addEventListener('dragleave', handleDragLeave);
  dropzone2.addEventListener('drop', function(e) {
    handleDrop(e, fileInput2, fileNameDisplay2);
  });
});


// elem = document.getElementById('time');

// async function update() {
//     let res = await fetch('/api/upload');
//     let json = await res.json();
//     elem.innerHTML = json.message;
// }


// setInterval(update, 1000);
