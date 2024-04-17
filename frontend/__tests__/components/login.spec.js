import { shallowMount } from '@vue/test-utils';
import TheLoginView from '@/views/TheLoginView.vue';
import axios from 'axios';

jest.mock('axios');

describe('TheLoginView.vue', () => {
  it('submits login form data successfully', async () => {
    const wrapper = shallowMount(TheLoginView, {
      mocks: {
        $t: () => {}
      },
      stubs: ['router-link']
    });

    // Set form data
    await wrapper.setData({
      authValue: "test@example.com",
      password: "password123"
    });

    // Mock axios post request
    axios.post.mockResolvedValueOnce({ data: { token: 'token', id: 'userId' } });

    // Call the submitForm function
    await wrapper.vm.submitForm();

    // Expectations
    expect(wrapper.vm.waitingFormResponse).toBe(false); // waitingFormResponse should be reset
    expect(wrapper.vm.showDisabledAccountLink).toBe(false); // showDisabledAccountLink should be reset
    expect(wrapper.vm.showScheduledDeletionAccountLink).toBe(false); // showScheduledDeletionAccountLink should be reset
  });

  it('handles login form submission errors', async () => {
    const wrapper = shallowMount(TheLoginView, {
      mocks: {
        $t: () => {}
      },
      stubs: ['router-link']
    });

    // Set form data
    await wrapper.setData({
      authValue: "test@example.com",
      password: "password123"
    });

    // Mock axios post request to throw an error
    const errorMessage = 'Error message';
    axios.post.mockRejectedValueOnce({ response: { data: { error: errorMessage } } });

    // Call the submitForm function
    await wrapper.vm.submitForm();

    // Expectations
    expect(wrapper.vm.waitingFormResponse).toBe(false); // waitingFormResponse should be reset
    expect(wrapper.vm.showDisabledAccountLink).toBe(false); // showDisabledAccountLink should be reset
    expect(wrapper.vm.showScheduledDeletionAccountLink).toBe(false); // showScheduledDeletionAccountLink should be reset
  });
});
