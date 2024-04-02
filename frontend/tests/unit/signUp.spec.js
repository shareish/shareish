import { shallowMount } from '@vue/test-utils'
import TheSignUpView from '@/views/TheSignUpView.vue'
import axios from 'axios';

jest.mock('axios');

describe('TheSignUpView.vue', () => {
  it('test the content of registration form fields', async () => {
    const wrapper = shallowMount(TheSignUpView,{
        mocks:{
            $t: () => {}
          },
          stubs:['router-link']
    })
    await wrapper.setData({
        email: "test@test.com",
        username : "username",
        first_name: 'user',
        last_name: 'name',
        password: 'password123',
        agreement: true

    })
    expect((wrapper.find("#email")).html()).toContain("test@test.com");
    expect((wrapper.find("#username")).html()).toContain("username");
    expect((wrapper.find("#firstname")).html()).toContain("user");
    expect((wrapper.find("#lastname")).html()).toContain("name");
    expect((wrapper.find("#password")).html()).toContain("password123");
    expect((wrapper.find("#agreement")).html()).toContain("true");

  });
  
  it('submits form data successfully', async () => {
    const wrapper = shallowMount(TheSignUpView,{
        mocks:{
            $t: () => {}
          },
          stubs:['router-link']
    })

    await wrapper.setData({
        email: "test@test.com",
        username : "username",
        first_name: 'user',
        last_name: 'name',
        password: 'password123',
        agreement: true

    })

    // Mock axios post request
    axios.post.mockResolvedValueOnce();

    // Call the submitForm function
    await wrapper.vm.submitForm();

    // Expectations
    expect(wrapper.vm.waitingFormResponse).toBe(false); // waitingFormResponse should be reset
    expect(wrapper.vm.errors).toHaveLength(0); // No errors should be present
  });

  it('handles form submission errors', async () => {

    const wrapper = shallowMount(TheSignUpView,{
        mocks:{
            $t: () => {}
          },
          stubs:['router-link']
    })

    // Mock form data
    await wrapper.setData({
        email: "test@test.com",
        username : "username",
        first_name: 'user',
        last_name: 'name',
        password: 'password123',
        agreement: true

    })

    // Mock axios post request to throw an error
    const errorMessage = 'Error message';
    const fail = 'err'
    axios.post.mockRejectedValueOnce({ response: { data: { error: errorMessage } } });

    // Call the submitForm function
    await wrapper.vm.submitForm();

    // Expectations
    expect(wrapper.vm.waitingFormResponse).toBe(false); // waitingFormResponse should be reset
    expect(wrapper.vm.errors).toContain(`error: ${errorMessage}`); // Error message should be added to errors array
  });
  
});
