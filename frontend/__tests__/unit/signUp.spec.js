import {mount} from '@vue/test-utils';
import TheSignUpView from '@/views/TheSignUpView.vue';

describe('TheSignUpView.vue', () => {
    it('test the content of registration form fields', async () => {
      const wrapper = mount(TheSignUpView,{
          mocks:{
              $t: () => {}
            },
            stubs:['router-link']
      })

      // values that will be transmitted to the fields
      const valueEmailInput = "test@test.com";
      const valueUsernameInput = "username";
      const valueFirstnameInput = "user";
      const valueLastnameInput = "name";
      const valuePasswordInput = "password123";
      const valueAgreementCheckBox = true;

      const inputEmail = wrapper.find('input#email');
      inputEmail.setValue(valueEmailInput);

      const inputUsername = wrapper.find('input#username');
      inputUsername.setValue(valueUsernameInput);

      const inputFirstName = wrapper.find('input#firstname');
      inputFirstName.setValue(valueFirstnameInput);

      const inputLastName = wrapper.find('input#lastname');
      inputLastName.setValue(valueLastnameInput);

      const inputPassword = wrapper.find('input#password');
      inputPassword.setValue(valuePasswordInput);

      const checkBoxAgreement = wrapper.find('#agreement');

      if(valueAgreementCheckBox){
        await checkBoxAgreement.trigger('click');
      }

      await wrapper.vm.$nextTick();
      
      // input fields tests
      expect(inputEmail.element.value).toBe(valueEmailInput);
      expect(inputUsername.element.value).toBe(valueUsernameInput);
      expect(inputFirstName.element.value).toBe(valueFirstnameInput);
      expect(inputLastName.element.value).toBe(valueLastnameInput);
      expect(inputPassword.element.value).toBe(valuePasswordInput);

      //models tests
      expect(wrapper.vm.agreement).toBe(!valueAgreementCheckBox);
      expect(wrapper.vm.email).toBe(valueEmailInput);
      expect(wrapper.vm.password).toBe(valuePasswordInput);
      expect(wrapper.vm.username).toBe(valueUsernameInput);
      expect(wrapper.vm.first_name).toBe(valueFirstnameInput);
      expect(wrapper.vm.last_name).toBe(valueLastnameInput);
    });
});