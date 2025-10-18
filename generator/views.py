import io
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, FileResponse
from .forms import QRForm
import qrcode
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H
from PIL import Image

EC_MAP = {
    'L': ERROR_CORRECT_L,
    'M': ERROR_CORRECT_M,
    'Q': ERROR_CORRECT_Q,
    'H': ERROR_CORRECT_H,
}

def make_qr_image(data, box_size=10, border=4, error_correction='M', logo_file=None):
    ec = EC_MAP.get(error_correction, ERROR_CORRECT_M)
    qr = qrcode.QRCode(
        error_correction=ec,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")

    if logo_file:
        try:
            logo = Image.open(logo_file).convert("RGBA")
            # Resize logo - make it at most 20% of QR size
            qr_w, qr_h = img.size
            factor = 5  # logo will be 1/factor of QR width (adjustable)
            max_logo_size = qr_w // factor
            logo.thumbnail((max_logo_size, max_logo_size), Image.ANTIALIAS)

            # calculate position and paste
            lx = (qr_w - logo.width) // 2
            ly = (qr_h - logo.height) // 2

            # If logo has alpha, composite properly
            img.paste(logo, (lx, ly), logo)
        except Exception:
            # fail gracefully: return QR without logo
            pass

    return img

def index(request):
    if request.method == "POST":
        form = QRForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data['data']
            box_size = form.cleaned_data['box_size']
            border = form.cleaned_data['border']
            ec = form.cleaned_data['error_correction']
            logo = form.cleaned_data.get('logo')

            img = make_qr_image(data, box_size=box_size, border=border, error_correction=ec, logo_file=logo)

            # Return inline preview page with image encoded as data URI (simple)
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)
            import base64
            img_b64 = base64.b64encode(buffer.getvalue()).decode()
            mime = "image/png"
            data_uri = f"data:{mime};base64,{img_b64}"

            context = {
                "form": form,
                "qr_data_uri": data_uri,
                "download_url": None,  # We'll provide a download via another view if desired
            }
            return render(request, "generator/result.html", context)
    else:
        form = QRForm()

    return render(request, "generator/index.html", {"form": form})

# API endpoint that returns raw PNG (POST JSON or form)
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def api_generate_png(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Use POST")

    # Accept JSON or form-data
    data = request.POST.get('data')
    if not data:
        try:  
            payload = json.loads(request.body.decode() or "{}")
            data = payload.get('data')
        except Exception:
            data = None

    if not data:
        return HttpResponseBadRequest("No 'data' provided")

    box_size = int(request.POST.get('box_size', 10))
    border = int(request.POST.get('border', 4))
    ec = request.POST.get('error_correction', 'M')
    logo = request.FILES.get('logo')  # optional

    img = make_qr_image(data, box_size=box_size, border=border, error_correction=ec, logo_file=logo)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='qrcode.png', content_type='image/png')


def info(request):
    return render(request, "generator/info.html")
