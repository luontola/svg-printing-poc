export async function saveAsPng(element) {
  console.log(element);

  let imageElement;
  if (element instanceof HTMLImageElement) {
    imageElement = element;
  } else if (element instanceof SVGSVGElement) {
    imageElement = await svgToImage(element);
  } else if (element instanceof HTMLObjectElement) {
    imageElement = await svgToImage(element.contentDocument.documentElement);
  } else {
    throw Error("Unsupported element " + element.constructor.name)
  }

  const canvas = renderToCanvas(imageElement);
  const dataUrl = canvas.toDataURL('image/png');
  triggerDownload(dataUrl, "image.png")
}

function svgToImage(svgElement) {
  const svg = new XMLSerializer().serializeToString(svgElement);
  return new Promise((resolve, reject) => {
    const image = new Image();
    image.onload = () => {
      resolve(image);
    };
    image.onerror = () => {
      reject(new Error("svgToImage failed"));
    }
    image.src = 'data:image/svg+xml;base64,' + btoa(svg);
  });
}

function renderToCanvas(imageElement, dpi = 300) {
  const connected = imageElement.isConnected;
  if (!connected) {
    // the image must be in the DOM, or its width and height will be zero
    document.body.appendChild(imageElement);
  }
  const imageWidth = imageElement.clientWidth;
  const imageHeight = imageElement.clientHeight;
  if (!connected) {
    document.body.removeChild(imageElement);
  }

  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');

  // calculate the dimensions for the canvas to achieve target DPI
  const scaleFactor = dpi / screenDpi();
  canvas.width = imageWidth * scaleFactor;
  canvas.height = imageHeight * scaleFactor;
  canvas.style.width = `${imageWidth}px`;
  canvas.style.height = `${imageHeight}px`;

  // scale the original image to the canvas DPI
  ctx.scale(scaleFactor, scaleFactor);

  ctx.drawImage(imageElement, 0, 0);
  return canvas;
}

function screenDpi() {
  return document.getElementById("dpi").offsetHeight; // typically 96
}

function triggerDownload(dataUrl, filename) {
  const link = document.createElement('a');
  link.href = dataUrl;
  link.download = filename;
  link.click();
}
    