
from scipy import ndimage
from skimage.filter import canny
from skimage.filter import sobel
from skimage import morphology
from skimage.measure import regionprops


def label_and_centerpoints(cleaned_data):
    labeled_image, _ = ndimage.label(cleaned_data)
    centroids_x = []
    centroids_y = []
    bounds = []
    for region in regionprops(labeled_image):
        # These were reversed for some reason?
        centroids_x.append(int(region.centroid[1]))
        centroids_y.append(int(region.centroid[0]))
        bounds.append(region.bbox)
    return centroids_x, centroids_y, bounds

def find_canny_edge_locations(image_data):
    edges = canny(image_data / 255.0, low_threshold=0.0, high_threshold=0.0)
    fill_data = ndimage.binary_fill_holes(edges)
    cleaned_data = morphology.remove_small_objects(fill_data, 150)
    return cleaned_data

def filter_boxes(bounds, size_threshold):
    large_bounds = []
    for bounding_box in bounds:
        minr, minc, maxr, maxc = bounding_box
        if (maxr - minr) * (maxc - minc) < size_threshold:
            continue
        else:
            large_bounds.append(bounding_box)

    width_and_heights = []
    final_boxes = []
    for bounding_box in large_bounds:
        minr, minc, maxr, maxc = bounding_box
        width = maxc - minc
        height = maxr - minr

        # add the first one
        if not width_and_heights:
            width_and_heights.append((width, height))
            continue

        delta = 15
        for test_width, test_height in width_and_heights:
            if width > test_width - delta and width < test_width + delta:
                width_and_heights.append((width, height))
                final_boxes.append(bounding_box)
                break
    # this is x1, y1, x2, y2
    return final_boxes


def get_objects_as_boxes(image_data):
    # So far, it looks like canny edge detection is the best
    canny_segments = find_canny_edge_locations(image_data)
    centroids_x, centroids_y, bounds = label_and_centerpoints(canny_segments)

    size_threshold = 750
    final_boxes = filter_boxes(bounds, size_threshold)
    return final_boxes

def create_button_data(data):
    # Format data to our specs
    button_data = []
    for x1, y1, x2, y2 in data:
        location = {'x':  int(x1 + x2 / 2), 'y': int(y1 + y2 / 2)}
        radius = {'x':  int(x2 - x1), 'y': int(y2 - y1)}
        button_data.append({'location': location, 'radius': radius})

    return button_data

def image_to_button_data(image_data):
    box_data = get_objects_as_boxes(image_data)
    button_data = create_button_data(box_data)
    return button_data