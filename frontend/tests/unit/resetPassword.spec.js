import { shallowMount } from "@vue/test-utils";
import TheResetPasswordView from "@/views/TheResetPasswordView.vue";
import axios from 'axios';

jest.mock('axios');

describe('TheResetPasswordView.vue', () => {
    it('test the submitForm function - success case', async () => {
        const wrapper = shallowMount(TheResetPasswordView, {
            mocks: {
                $t: () => {},
                $router: {
                    push: jest.fn() // Mocking router push method
                },
                $buefy: {
                    snackbar: {
                        open: jest.fn() // Mocking snackbar open method
                    }
                }
            },
        });

        // Mocking email data
        await wrapper.setData({
            email : "test@test.com"
        });

        // Mocking axios post method
        axios.post.mockResolvedValueOnce({});

        // Triggering the submitForm method
        await wrapper.vm.submitForm();

        // Asserting that axios post method was called with correct arguments
        expect(axios.post).toHaveBeenCalledWith("/api/v1/users/reset_password/", { email: "test@test.com" });

        // Asserting that snackbar open method was called with correct arguments
        expect(wrapper.vm.$buefy.snackbar.open).toHaveBeenCalledWith({
            duration: 5000,
            type: 'is-success',
            message: wrapper.vm.$t('notif-success-password-reset-sent'),
            pauseOnHover: true
        });

        // Asserting that router push method was called with correct argument
        expect(wrapper.vm.$router.push).toHaveBeenCalledWith('/log-in');

        // Asserting that waitingFormResponse is set to false after function execution
        expect(wrapper.vm.waitingFormResponse).toBe(false);
    });

    it('test the submitForm function - error case', async () => {
        const wrapper = shallowMount(TheResetPasswordView, {
            mocks: {
                $t: () => {},
                $router: {
                    push: jest.fn() // Mocking router push method
                },
                $buefy: {
                    snackbar: {
                        open: jest.fn() // Mocking snackbar open method
                    }
                }
            },
        });
    
        // Mocking email data
        await wrapper.setData({
            email : "test@test.com"
        });
    
        // Mocking axios post method to throw an error
        axios.post.mockRejectedValueOnce(new Error('Failed to reset password'));
    
        // Triggering the submitForm method
        await wrapper.vm.submitForm();
    
        // Asserting that axios post method was called with correct arguments
        expect(axios.post).toHaveBeenCalledWith("/api/v1/users/reset_password/", { email: "test@test.com" });
    
        // Asserting that snackbar open method was not called with any arguments
        expect(wrapper.vm.$buefy.snackbar.open).not.toHaveBeenCalledWith();
    
        // Asserting that router push method was not called
        expect(wrapper.vm.$router.push).not.toHaveBeenCalled();
    
        // Asserting that waitingFormResponse is set to false after function execution
        expect(wrapper.vm.waitingFormResponse).toBe(false);
    });    
});
