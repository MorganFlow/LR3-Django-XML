import os
import xml.etree.ElementTree as ET
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponseBadRequest
from .forms import TourForm, UploadXMLForm
from .utils import FIELDS

def get_xml_dir():
    xml_dir = os.path.join(settings.MEDIA_ROOT, 'xml_data')
    if not os.path.exists(xml_dir):
        os.makedirs(xml_dir)
    return xml_dir

def get_xml_path():
    return os.path.join(get_xml_dir(), 'tours.xml')

def validate_tour_data(data):
    for field_name, field_info in FIELDS.items():
        value = data.get(field_name)
        if field_info['required'] and value is None:
            raise ValueError(f"Поле '{field_name}' обязательно.")
        if value is not None:
            if field_info['type'] == str:
                if 'max_length' in field_info and len(value) > field_info['max_length']:
                    raise ValueError(f"Поле '{field_name}' превышает максимальную длину.")
                if 'choices' in field_info and value not in field_info['choices']:
                    raise ValueError(f"Недопустимое значение для '{field_name}'.")
            elif field_info['type'] == int:
                try:
                    int_value = int(value)
                    if 'min_value' in field_info and int_value < field_info['min_value']:
                        raise ValueError(f"Поле '{field_name}' должно быть не менее {field_info['min_value']}.")
                except ValueError:
                    raise ValueError(f"Поле '{field_name}' должно быть целым числом.")
            elif field_info['type'] == float:
                try:
                    float_value = float(value)
                    if 'min_value' in field_info and float_value < field_info['min_value']:
                        raise ValueError(f"Поле '{field_name}' должно быть не менее {field_info['min_value']}.")
                except ValueError:
                    raise ValueError(f"Поле '{field_name}' должно быть числом.")

def append_to_xml(new_tours):
    file_path = get_xml_path()
    
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                content = f.read().strip()
                if not content:
                    raise ET.ParseError("Empty file")
            tree = ET.parse(file_path)
            root = tree.getroot()
        except (ET.ParseError, FileNotFoundError):
            root = ET.Element('tours')
            tree = ET.ElementTree(root)
    else:
        root = ET.Element('tours')
        tree = ET.ElementTree(root)
    
    for tour in new_tours:
        root.append(tour)
    
    tree.write(file_path, encoding='utf-8', xml_declaration=True)

def add_tour(request):
    if request.method == 'POST':
        form = TourForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                validate_tour_data(data)
                # Создать элемент tour
                tour = ET.Element('tour')
                for field_name in FIELDS:
                    ET.SubElement(tour, field_name).text = str(data[field_name])
                append_to_xml([tour])
                return redirect('tour_list')
            except ValueError as e:
                return HttpResponseBadRequest(str(e))
    else:
        form = TourForm()
    return render(request, 'myapp/add_tour.html', {'form': form})

def upload_xml(request):
    if request.method == 'POST':
        form = UploadXMLForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            if not uploaded_file.name.endswith('.xml'):
                return HttpResponseBadRequest('Файл должен быть в формате XML.')
            
            try:
                # Парсим загруженный XML в памяти
                uploaded_content = uploaded_file.read().decode('utf-8')
                uploaded_tree = ET.ElementTree(ET.fromstring(uploaded_content))
                uploaded_root = uploaded_tree.getroot()
                if uploaded_root.tag != 'tours':
                    raise ValueError('Корневой элемент должен быть "tours".')
                
                new_tours = []
                for tour in uploaded_root.findall('tour'):
                    tour_data = {child.tag: child.text for child in tour}
                    validate_tour_data(tour_data)
                    new_tours.append(tour)
                
                if new_tours:
                    append_to_xml(new_tours)
                    return redirect('tour_list')
                else:
                    return HttpResponseBadRequest('В файле нет валидных записей о турах.')
            except (ET.ParseError, ValueError) as e:
                return HttpResponseBadRequest(f'Невалидный XML: {str(e)}')
    else:
        form = UploadXMLForm()
    return render(request, 'myapp/upload_xml.html', {'form': form})

def tour_list(request):
    file_path = get_xml_path()
    all_tours = []
    no_files = not os.path.exists(file_path)
    
    if not no_files:
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            for tour in root.findall('tour'):
                tour_data = {child.tag: child.text for child in tour if child.tag in FIELDS}
                all_tours.append(tour_data)
        except ET.ParseError:
            no_files = True
    
    return render(request, 'myapp/tour_list.html', {
    'tours': all_tours, 
    'no_files': no_files, 
    'fields': list(FIELDS.keys()),
    'field_labels': {k: v['label'] for k, v in FIELDS.items()}
})