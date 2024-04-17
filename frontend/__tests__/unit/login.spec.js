import {mount} from '@vue/test-utils';
import TheLoginView from '@/views/TheLoginView.vue';

describe("TheLoginView unit test",() => {
    it("test fields of login form", () => {

        // values that will be transmitted to the fields
        const valueUsernameInput = 'testUser';
        const valuePasswordInput = 'testPassword';

        const wrapper = mount(TheLoginView,{
            mocks: { $t : () => {}},
            stubs : ['router-link']
        });

        const inputUsername = wrapper.find('input#username');
        inputUsername.setValue(valueUsernameInput);

        const inputPassword = wrapper.find('input#password');
        inputPassword.setValue(valuePasswordInput);

        expect(inputUsername.element.value).toBe(valueUsernameInput);
        expect(inputPassword.element.value).toBe(valuePasswordInput);

        expect(wrapper.vm.authValue).toBe(valueUsernameInput);
        expect(wrapper.vm.password).toBe(valuePasswordInput);
    });
})