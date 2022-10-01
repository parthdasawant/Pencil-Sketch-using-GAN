const cameraBtn = document.getElementById('cameraBtn')
const captureBtn = document.getElementById('capture')
const cancelBtn = document.getElementById('cancel')
const uploadBtn = document.getElementById('upload')
const fileInputBtn = document.getElementById('fileInput')
const videoElement = document.getElementById('video')
const videoContainer = document.getElementById('video-container')
const image = document.querySelector('.uploaded-image')

let stream

function startCamera() {
  let vendorURL = window.URL || window.webkitURL
  if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(stream => {
        video.srcObject = stream
        videoContainer.style.display = 'flex'
      })
      .catch(error => {
        cameraBtn.click()
        console.log(error)
      })
  }
}

function closeCamera() {
  let stream = video.srcObject
  let tracks = stream.getTracks()
  for (let i = 0; i < tracks.length; i++) {
    let track = tracks[i]
    track.stop()
  }
  video.srcObject = null
  videoContainer.style.display = 'none'
}

function captureImage() {
  const canvas = document.createElement('canvas')
  canvas.getContext('2d').drawImage(videoElement, 0, 0, 500, 500)
  let image_data_url = canvas.toDataURL('image/jpeg')

  console.log(image_data_url)

  closeCamera()
}

function uploadImage() {
  fileInputBtn.click()
}

cameraBtn.addEventListener('click', startCamera)
cancelBtn.addEventListener('click', closeCamera)
captureBtn.addEventListener('click', captureImage)
// uploadBtn.addEventListener('click', uploadImage)
fileInputBtn.addEventListener('change', (e) => {
  console.log(this.files)
  // const file = this.file[0]
  // console.log()
  // if (file) {
  //   const reader = new FileReader()
  //   reader.onload = function() {
  //     const result = reader.result
  //     image.src = result
  //   }
  //   reader.readAsDataURL(file)
  //   image.style.display = 'block'
  // }
  image.src = e.target.value
  image.style.display = 'block'
})