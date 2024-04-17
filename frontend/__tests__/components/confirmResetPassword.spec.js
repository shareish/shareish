import { shallowMount } from "@vue/test-utils";
import TheResetPasswordConfirmView from "@/views/TheResetPasswordConfirmView.vue";
import axios from 'axios';

jest.mock('axios');

describe('TheResetPasswordConfirmView.vue', () => {
    it('test the submitForm function - success case', async () => {
        const mockRoute = {
            params: {
                uid: 'test_uid',
                token: 'test_token'
            }
        };

        const wrapper = shallowMount(TheResetPasswordConfirmView, {
            mocks: {
                $t: () => {},
                $router: {
                    push: jest.fn() // Mocking router push method
                },
                $route: mockRoute,
                $buefy: {
                    snackbar: {
                        open: jest.fn() // Mocking snackbar open method
                    }
                }
            },
        });

        // Mocking password data
        await wrapper.setData({
            password : "test_password"
        });

        // Mocking axios post method to resolve successfully
        axios.post.mockResolvedValueOnce({});

        // Triggering the submitForm method
        await wrapper.vm.submitForm();

        // Asserting that axios post method was called with correct arguments
        expect(axios.post).toHaveBeenCalledWith("/api/v1/users/reset_password_confirm/", {
            uid: 'test_uid',
            token: 'test_token',
            new_password: 'test_password'
        });

        // Asserting that snackbar open method was called with correct arguments
        expect(wrapper.vm.$buefy.snackbar.open).toHaveBeenCalledWith({
            duration: 5000,
            type: 'is-success',
            message: wrapper.vm.$t('notif-success-password-reset'),
            pauseOnHover: true
        });

        // Asserting that router push method was called with correct argument
        expect(wrapper.vm.$router.push).toHaveBeenCalledWith('/log-in');

        // Asserting that waitingFormResponse is set to false after function execution
        expect(wrapper.vm.waitingFormResponse).toBe(false);
    });

    it('test the submitForm function - error case', async () => {
        const mockRoute = {
            params: {
                uid: 'test_uid',
                token: 'test_token'
            }
        };
        
        const wrapper = shallowMount(TheResetPasswordConfirmView, {
            mocks: {
                $t: () => {},
                $router: {
                    push: jest.fn() // Mocking router push method
                },
                $route: mockRoute,
                $buefy: {
                    snackbar: {
                        open: jest.fn() // Mocking snackbar open method
                    }
                }
            },
        });

        // Mocking password data
        await wrapper.setData({
            password : "test_password"
        });

        // Mocking axios post method to reject with an error
        axios.post.mockRejectedValueOnce(new Error('Failed to reset password'));

        // Triggering the submitForm method
        await wrapper.vm.submitForm();

        // Asserting that axios post method was called with correct arguments
        expect(axios.post).toHaveBeenCalledWith("/api/v1/users/reset_password_confirm/", {
            uid: 'test_uid',
            token: 'test_token',
            new_password: 'test_password'
        });

        // Asserting that snackbar open method was not called
        expect(wrapper.vm.$buefy.snackbar.open).not.toHaveBeenCalledWith({
            duration: 5000,
            type: 'is-success',
            message: wrapper.vm.$t('notif-success-password-reset'),
            pauseOnHover: true
        });
        // Asserting that router push method was not called
        expect(wrapper.vm.$router.push).not.toHaveBeenCalled();

        // Asserting that waitingFormResponse is set to false after function execution
        expect(wrapper.vm.waitingFormResponse).toBe(false);
    });
});
