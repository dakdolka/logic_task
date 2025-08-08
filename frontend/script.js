document.addEventListener('DOMContentLoaded', function () {
  const uploadButton = document.getElementById('uploadAllFiles');
  const fileInput1 = document.getElementById('file1');
  const fileInput2 = document.getElementById('file2');
  const selectFileButton1 = document.getElementById('selectFile1');
  const selectFileButton2 = document.getElementById('selectFile2');
  const fileNameDisplay1 = document.getElementById('fileName1');
  const fileNameDisplay2 = document.getElementById('fileName2');
  const loginForm = document.querySelector('.login-form');

  // Проверка авторизации при загрузке страницы
  if (localStorage.getItem('is_logined') === 'true') {
    console.log('Пользователь авторизован');
  } else {
    console.log('Пользователь не авторизован');
  }

  loginForm.addEventListener('submit', function (event) {
    event.preventDefault();  // отменяем перезагрузку страницы

    const username = loginForm.username.value;
    const password = loginForm.password.value;

    login(username, password);
  });

  function updateFileNameDisplay(inputElement, displayElement) {
    const file = inputElement.files[0];
    if (file) {
      displayElement.textContent = file.name;
    } else {
      displayElement.textContent = "Выберите файл";
    }
  }

  function uploadFiles(file1, file2) {
    if (localStorage.getItem('is_logined') !== 'true') {
      alert('Сначала авторизуйтесь!');
      return;
    }

    const formData = new FormData();
    formData.append('file1', file1);
    formData.append('file2', file2);

    fetch('http://192.168.88.18/api/upload', {
      method: 'POST',
      body: formData
    })
      .then(res => res.json())
      .then(data => {
        alert("Файлы загружены. Теперь можно получить результат.");
        document.getElementById("get-result-btn").classList.remove("hidden");
      })
      .catch(err => {
        console.error(err);
        alert('Ошибка при загрузке');
      });
  }

  uploadButton.addEventListener('click', function () {
    const file1 = fileInput1.files[0];
    const file2 = fileInput2.files[0];

    if (!file1 || !file2) {
      alert('Пожалуйста, выберите оба файла перед отправкой.');
      return;
    }

    uploadFiles(file1, file2);
  });

  selectFileButton1.addEventListener('click', function () {
    fileInput1.click();
  });

  selectFileButton2.addEventListener('click', function () {
    fileInput2.click();
  });

  fileInput1.addEventListener('change', function () {
    updateFileNameDisplay(fileInput1, fileNameDisplay1);
  });

  fileInput2.addEventListener('change', function () {
    updateFileNameDisplay(fileInput2, fileNameDisplay2);
  });

  function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
  }

  function handleDragOver(e) {
    preventDefaults(e);
    e.target.classList.add('dragover');
  }

  function handleDragLeave(e) {
    preventDefaults(e);
    e.target.classList.remove('dragover');
  }

  function handleDrop(e, fileInput, fileNameDisplay) {
    preventDefaults(e);
    e.target.classList.remove('dragover');

    const file = e.dataTransfer.files[0];
    if (file) {
      fileInput.files = e.dataTransfer.files;
      updateFileNameDisplay(fileInput, fileNameDisplay);
    }
  }

  const dropzone1 = document.getElementById('dropzone1');
  const dropzone2 = document.getElementById('dropzone2');

  dropzone1.addEventListener('dragover', handleDragOver);
  dropzone1.addEventListener('dragleave', handleDragLeave);
  dropzone1.addEventListener('drop', function (e) {
    handleDrop(e, fileInput1, fileNameDisplay1);
  });

  dropzone2.addEventListener('dragover', handleDragOver);
  dropzone2.addEventListener('dragleave', handleDragLeave);
  dropzone2.addEventListener('drop', function (e) {
    handleDrop(e, fileInput2, fileNameDisplay2);
  });
});

async function getResultFile() {
  if (localStorage.getItem('is_logined') !== 'true') {
    alert('Сначала авторизуйтесь!');
    return;
  }

  try {
    const response = await fetch('http://192.168.88.18/api/get_res');

    if (!response.ok) {
      throw new Error('Ошибка при получении файла');
    }

    const name = response.headers.get('Content-Disposition') || 'result.txt';
    const blob = await response.blob();

    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = name;
    document.body.appendChild(a);
    a.click();
    a.remove();
  } catch (err) {
    console.error(err);
    alert('Ошибка при скачивании файла');
  }
}

async function login(username, password) {
  try {
    const response = await fetch('http://localhost:8000/api/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ username, password })
    });

    const data = await response.json();
    console.log(data);

    if (data.success ||  data === true) {
      localStorage.setItem('is_logined', 'true');
      alert('Вы успешно вошли!');
    } else {
      alert('Неверный логин или пароль');
    }
  } catch (err) {
    console.error(err);
    alert('Ошибка при входе');
  }
}
