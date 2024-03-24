import { shallowMount } from '@vue/test-utils';
import TheAddItemView from '@/views/TheAddItemView.vue';
import axios from 'axios';


// Mocking axios.post
jest.mock('axios', () => ({
  post: jest.fn(),
}));

// Mocking GeolocationCoords
jest.mock('@/functions', () => ({
  GeolocationCoords: jest.fn().mockImplementation(() => ({
    update: jest.fn(),
    toStringForUser: jest.fn()
  })),
}));

describe('TheAddItemView', () => {
  let wrapper;

  beforeEach(() => {
    // Mock $route.params
    const $route = {
      params: {
        type: 'yourType',
        lat: 123, // Example latitude value
        lng: 456, // Example longitude value
        resource: 'yourResource',
        rid: 'yourRid',
      },
    };

    wrapper = shallowMount(TheAddItemView, {
      mocks: {
        $route,
        $t : () => {}
      },
      stubs: ['router-link'],
    });
  });

  afterEach(() => {
    // Clear all mocks after each test
    jest.clearAllMocks();
  });

  it('submits form successfully', async () => {
    // Mock validation result to be true
    wrapper.vm.$validator.validateAll = jest.fn(() => true);

    // Mock response data from axios.post
    const responseData = { id: 123 };
    axios.post.mockResolvedValueOnce({ data: responseData });

    // Mock images array
    wrapper.setData({ images: [{ preview: 'image1.jpg', filename: 'image1' }] });

    // Trigger the submit method
    await wrapper.vm.submit();

    // Check if axios.post was called with the correct arguments
    expect(axios.post).toHaveBeenCalledWith('/api/v1/items/', {
      name: wrapper.vm.name,
      type: wrapper.vm.type,
      category1: wrapper.vm.category1,
      category2: wrapper.vm.category2,
      category3: wrapper.vm.category3,
      description: wrapper.vm.description,
      location: wrapper.vm.address,
      use_coordinates: wrapper.vm.use_coordinates,
      is_recurrent: wrapper.vm.isRecurrent,
      startdate: expect.any(String),
      enddate: expect.any(String),
      visibility: wrapper.vm.visibility,
      images: [],
    });

    // Check if the router was pushed to the correct path
    expect(wrapper.vm.$router.push).toHaveBeenCalledWith('/items/123');
  });

  it('handles submission error', async () => {
    // Mock validation result to be true
    wrapper.vm.$validator.validateAll = jest.fn(() => true);

    // Mock error response from axios.post
    const errorMessage = 'Submission failed';
    axios.post.mockRejectedValueOnce(new Error(errorMessage));

    // Trigger the submit method
    await wrapper.vm.submit();

    // Check if snackbarError was called with the correct error message
    expect(wrapper.vm.snackbarError).toHaveBeenCalledWith(new Error(errorMessage));
  });
});
