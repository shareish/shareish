import {mount} from '@vue/test-utils';
import TheSettingsAccount from '@/components/TheSettingsAccount.vue';

describe('TheSettingsAccount.vue', () => { 
    it('test the content of account settings form fields', async () => {
        const wrapper = mount(TheSettingsAccount,{
            mocks:{
                $t: () => {}
            },
            propsData: {
                user: {
                    first_name: 'user',
                    last_name: 'name',
                    username: 'username',
                    email: 'test@gmail.com',
                    save_item_viewing : 'yes'
                }
            }
        });

        const EmailInput = wrapper.find('input#email');
        const UsernameInput = wrapper.find('input#username');
        const FirstNameInput = wrapper.find('input#firstname');
        const LastNameInput = wrapper.find('input#lastname');
        const SaveItemViewing = wrapper.find('button#save_item_viewing');
        
        expect(EmailInput.element.value).toBe('test@gmail.com');
        expect(wrapper.vm.internalUser['email']).toBe('test@gmail.com');

        expect(UsernameInput.element.value).toBe('username');
        expect(wrapper.vm.internalUser['username']).toBe('username');

        expect(FirstNameInput.element.value).toBe('user');
        expect(wrapper.vm.internalUser['first_name']).toBe('user');

        expect(LastNameInput.element.value).toBe('name');
        expect(wrapper.vm.internalUser['last_name']).toBe('name');

        expect(SaveItemViewing.classes()).toContain('is-success');
        await SaveItemViewing.trigger('click');
        expect(wrapper.vm.internalUser['save_item_viewing']).toBe(false);
        expect(SaveItemViewing.classes()).toContain('is-danger');
    });
});
